#!/usr/bin/env python3
"""Sign in to a remote MCP server that uses OAuth, and keep the sign-in in an
Orca vault as an `mcp_oauth` credential, so your agents can use the server.

    python scripts/connect_mcp_oauth.py --server https://connect.composio.dev/mcp --vault composio

It works with any MCP server that does OAuth with dynamic client
registration and PKCE (orca-design connected-apps D5.15):

1. Reads the server's OAuth metadata and registers a public client.
2. Opens your browser to sign in. The code comes back to 127.0.0.1 once,
   checked with PKCE (S256) and `state`, and the listener closes.
3. Creates the credential in the vault (creating the vault if it has no
   vault by that name), bound to the exact server URL, with the token
   endpoint so Orca refreshes the token itself. A credential for the same
   URL already in that vault is deleted after the new one is created.

The Orca key comes from ORCA_API_KEY, else the orca CLI's sign-in, else a
hidden prompt; it must be an admin's. Nothing secret is printed or written
to disk: only ids.
"""

import argparse
import base64
import datetime
import getpass
import hashlib
import http.server
import json
import os
import pathlib
import re
import secrets
import ssl
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

DEFAULT_API_URL = "https://api.orcapods.ai"
# The orca CLI's old default, which it upgrades on read (orca-cli src/lib/defaults.ts).
LEGACY_API_URL = "https://conductor-production-0859.up.railway.app"
CALLBACK_PATH = "/callback"
CALLBACK_TIMEOUT = 600
USER_AGENT = "orca-kits-connect/1.0"
LOOPBACK = {"127.0.0.1", "localhost", "::1"}


def ssl_context():
    # python.org builds on macOS ship without CA certificates.
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    if pathlib.Path("/etc/ssl/cert.pem").exists():
        return ssl.create_default_context(cafile="/etc/ssl/cert.pem")
    return ssl.create_default_context()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect, urllib.request.HTTPSHandler(context=ssl_context()))


def request(url, body=None, headers=None, form=False, method=None):
    """(status, headers, parsed JSON or None). Redirects are not followed."""
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT, **(headers or {})}
    data = None
    if body is not None:
        if form:
            data = urllib.parse.urlencode(body).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
    try:
        with OPENER.open(urllib.request.Request(url, data=data, headers=headers, method=method), timeout=60) as reply:
            status, reply_headers, raw = reply.status, reply.headers, reply.read()
    except urllib.error.HTTPError as error:
        status, reply_headers, raw = error.code, error.headers, error.read()
    except (urllib.error.URLError, OSError) as error:
        sys.exit(f"Could not reach {urllib.parse.urlsplit(url).netloc}: {getattr(error, 'reason', error)}")
    try:
        parsed = json.loads(raw) if raw.strip() else None
    except ValueError:
        parsed = None
    return status, reply_headers, parsed


def checked_url(url, what):
    """HTTPS, or plain HTTP on this machine only."""
    parts = urllib.parse.urlsplit(url or "")
    if not parts.hostname or not (parts.scheme == "https" or (parts.scheme == "http" and parts.hostname in LOOPBACK)):
        sys.exit(f"The {what} must be an HTTPS URL; got {url!r}.")
    return url


def same_url(a, b):
    """Equal once spelled the same way, as the server compares them."""

    def norm(url):
        parts = urllib.parse.urlsplit(url)
        port = parts.port if parts.port not in ({"https": 443, "http": 80}.get(parts.scheme), None) else None
        host = (parts.hostname or "") + (f":{port}" if port else "")
        return (parts.scheme.lower(), host.lower(), parts.path or "/", parts.query)

    try:
        return norm(a) == norm(b)
    except ValueError:
        return False


# Orca


def cli_context():
    """The orca CLI's current context, resolved as orca-cli's src/lib/config.ts does."""
    folder = os.environ.get("ORCA_CONFIG_DIR")
    if not folder:
        xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
        folder = os.path.join(xdg or os.path.join(pathlib.Path.home(), ".config"), "orca")
    try:
        config = json.loads((pathlib.Path(folder) / "config.json").read_text())
        name = os.environ.get("ORCA_CONTEXT") or config.get("currentContext") or "default"
        return config.get("contexts", {}).get(name) or {}
    except (OSError, ValueError, AttributeError):
        return {}


def orca_target():
    """(API URL, key): the key from ORCA_API_KEY, the CLI's sign-in, or a hidden prompt."""
    context = cli_context()
    url = os.environ.get("ORCA_API_URL") or context.get("apiUrl") or DEFAULT_API_URL
    if url.rstrip("/") == LEGACY_API_URL:
        url = DEFAULT_API_URL
    key = os.environ.get("ORCA_API_KEY") or context.get("apiKey")
    if not key:
        key = getpass.getpass("Orca API key (an admin's; it is not shown): ").strip()
    if not key:
        sys.exit("No Orca API key: set ORCA_API_KEY, run `orca auth login`, or paste one at the prompt.")
    return checked_url(url.rstrip("/"), "Orca API URL"), key


class Orca:
    def __init__(self, url, key):
        self.url, self.key = url, key

    def call(self, method, path, body=None):
        status, _, reply = request(f"{self.url}{path}", body, {"Authorization": f"Bearer {self.key}"}, method=method)
        if status >= 400:
            error = (reply or {}).get("error") if isinstance(reply, dict) else None
            message = error.get("message") if isinstance(error, dict) else None
            sys.exit(f"Orca {method} {path} failed: HTTP {status}{': ' + message if message else ''}")
        return reply or {}

    def every(self, path):
        rows, after = [], None
        while True:
            query = urllib.parse.urlencode({"limit": 100, **({"after": after} if after else {})})
            page = self.call("GET", f"{path}?{query}")
            rows.extend(page.get("data") or [])
            if not page.get("has_more") or not rows:
                return rows
            after = rows[-1]["id"]


def store(orca, vault_name, name, auth):
    vault = next((v for v in orca.every("/v1/vaults") if v.get("name") == vault_name), None)
    if vault is None:
        vault = orca.call("POST", "/v1/vaults", {"name": vault_name})
        print(f"Created vault {vault_name!r} ({vault['id']}).")
    path = f"/v1/vaults/{vault['id']}/credentials"
    # Two credentials for one URL in a session's vaults make the session fail,
    # so the old one goes, only after the new one exists.
    old = [c for c in orca.every(path) if same_url((c.get("auth") or {}).get("mcp_server_url") or "", auth["mcp_server_url"])]
    credential = orca.call("POST", path, {"name": name, "auth": auth})
    print(f"Added credential {name!r} ({credential['id']}) to vault {vault_name!r} ({vault['id']}).")
    for row in old:
        orca.call("DELETE", f"{path}/{row['id']}")
        print(f"Deleted the older credential for this server ({row['id']}).")


# OAuth


def discover(server):
    """The authorization server's metadata and the scope to ask for."""
    status, headers, _ = request(server, {"jsonrpc": "2.0", "id": 1, "method": "ping"}, {"Accept": "application/json, text/event-stream"}, method="POST")
    found = re.search(r'resource_metadata="([^"]+)"', headers.get("WWW-Authenticate", "") if headers else "")
    parts = urllib.parse.urlsplit(server)
    origin = f"{parts.scheme}://{parts.netloc}"
    candidates = [found.group(1)] if found else []
    candidates += [f"{origin}/.well-known/oauth-protected-resource{parts.path.rstrip('/')}", f"{origin}/.well-known/oauth-protected-resource"]
    resource = None
    for url in candidates:
        got, _, body = request(checked_url(url, "protected resource metadata URL"))
        if got == 200 and isinstance(body, dict) and body.get("authorization_servers"):
            resource = body
            break
    if resource is None:
        sys.exit(f"{server} published no OAuth metadata (HTTP {status} without sign-in); this script is for MCP servers that use OAuth.")
    if resource.get("resource") and not same_url(resource["resource"], server):
        sys.exit(f"The server's OAuth metadata is for {resource['resource']}, not {server}; stopping.")
    issuer = urllib.parse.urlsplit(checked_url(resource["authorization_servers"][0], "authorization server"))
    root, path = f"{issuer.scheme}://{issuer.netloc}", issuer.path.rstrip("/")
    meta = None
    for url in (f"{root}/.well-known/oauth-authorization-server{path}", f"{root}/.well-known/openid-configuration{path}", f"{root}{path}/.well-known/openid-configuration"):
        got, _, body = request(url)
        if got == 200 and isinstance(body, dict) and body.get("authorization_endpoint"):
            meta = body
            break
    if meta is None:
        sys.exit(f"Could not read the authorization server's metadata at {root}{path}.")
    if "S256" not in (meta.get("code_challenge_methods_supported") or []):
        sys.exit("The authorization server does not offer PKCE with S256; stopping.")
    for field in ("authorization_endpoint", "token_endpoint", "registration_endpoint"):
        if not meta.get(field):
            sys.exit(f"The authorization server has no {field}; this script needs dynamic client registration.")
        checked_url(meta[field], field.replace("_", " "))
    scopes = list(resource.get("scopes_supported") or [])
    # A refresh token usually needs offline_access.
    if "offline_access" in (meta.get("scopes_supported") or []) and "offline_access" not in scopes:
        scopes.append("offline_access")
    return meta, " ".join(scopes)


class Callback:
    """A listener on 127.0.0.1 that takes one sign-in reply, then closes."""

    def __init__(self):
        self.result = None
        self.done = threading.Event()
        listener = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                url = urllib.parse.urlsplit(self.path)
                query = dict(urllib.parse.parse_qsl(url.query))
                if listener.done.is_set() or url.path != CALLBACK_PATH or not ({"code", "error"} & set(query)):
                    self.send_response(404)
                    self.end_headers()
                    return
                listener.result = query
                listener.done.set()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<p>Done. You can close this tab and go back to the terminal.</p>")

        self.server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.server.server_address[1]
        self.redirect_uri = f"http://127.0.0.1:{self.port}{CALLBACK_PATH}"
        self.serving = False

    def start(self):
        self.serving = True
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        if self.serving:
            self.server.shutdown()
            self.serving = False
        self.server.server_close()

    def wait(self, state, timeout=CALLBACK_TIMEOUT):
        """The code from the first reply; exits on an error, a wrong state or the timeout."""
        try:
            arrived = self.done.wait(timeout)
        finally:
            self.close()
        if not arrived:
            sys.exit("No sign-in came back in time; nothing was stored.")
        reply = self.result
        if not secrets.compare_digest(reply.get("state", ""), state):
            sys.exit("The sign-in reply's state did not match; nothing was stored.")
        if "error" in reply:
            sys.exit(f"Sign-in refused: {reply['error']}; nothing was stored.")
        return reply["code"]


def pkce():
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def oauth_failure(step, status, reply):
    # Only the error code: a description or body could carry a code or a token.
    code = reply.get("error") if isinstance(reply, dict) and isinstance(reply.get("error"), str) else "no error code"
    sys.exit(f"{step} failed: HTTP {status}, {code}; nothing was stored.")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--server", required=True, help="the MCP server's URL, exactly as the agent's server_url has it")
    parser.add_argument("--vault", required=True, help="the Orca vault's name; created if there is none")
    parser.add_argument("--name", help="the credential's name (default: the server's host)")
    parser.add_argument("--scope", help="space-separated OAuth scopes (default: what the server publishes)")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    server = checked_url(args.server, "MCP server URL")
    orca = Orca(*orca_target())
    who = orca.call("GET", "/api/whoami")
    print(f"Orca organization {who.get('tenant')} ({orca.url}), signed in as {who.get('role')}.")
    if who.get("role") != "admin":
        sys.exit("Only an admin's key can add a credential; use an admin's key.")

    meta, scope = discover(server)
    scope = args.scope if args.scope is not None else scope
    listener = Callback()
    try:
        registration = {
            "client_name": "Orca",
            "redirect_uris": [listener.redirect_uri],
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
            "token_endpoint_auth_method": "none",
            **({"scope": scope} if scope else {}),
        }
        status, _, client = request(meta["registration_endpoint"], registration)
        if status >= 400 or not isinstance(client, dict) or not client.get("client_id"):
            oauth_failure("Client registration", status, client)
        verifier, challenge = pkce()
        state = secrets.token_urlsafe(32)
        query = {
            "response_type": "code",
            "client_id": client["client_id"],
            "redirect_uri": listener.redirect_uri,
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "resource": server,
            **({"scope": scope} if scope else {}),
        }
        split = urllib.parse.urlsplit(meta["authorization_endpoint"])
        authorize = urllib.parse.urlunsplit(split._replace(query="&".join(filter(None, [split.query, urllib.parse.urlencode(query)]))))
        listener.start()
        print(f"Sign in to {urllib.parse.urlsplit(server).netloc} in your browser. If it did not open, visit:\n\n{authorize}\n", flush=True)
        webbrowser.open(authorize)
        code = listener.wait(state)
    finally:
        listener.close()

    token_request = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": listener.redirect_uri,
        "client_id": client["client_id"],
        "code_verifier": verifier,
        "resource": server,
    }
    status, _, tokens = request(meta["token_endpoint"], token_request, form=True)
    if status >= 400 or not isinstance(tokens, dict) or not tokens.get("access_token"):
        oauth_failure("The token request", status, tokens)
    if str(tokens.get("token_type", "bearer")).lower() != "bearer":
        sys.exit("The server issued a token that is not a bearer token; nothing was stored.")

    auth = {"type": "mcp_oauth", "mcp_server_url": server, "access_token": tokens["access_token"]}
    if isinstance(tokens.get("expires_in"), int) and tokens["expires_in"] > 0:
        expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=tokens["expires_in"])
        auth["expires_at"] = expires.strftime("%Y-%m-%dT%H:%M:%SZ")
    if tokens.get("refresh_token"):
        auth["refresh"] = {
            "client_id": client["client_id"],
            "refresh_token": tokens["refresh_token"],
            "token_endpoint": meta["token_endpoint"],
            "token_endpoint_auth": {"type": "none"},
            "resource": server,
            "scope": tokens.get("scope") or scope or None,
        }
    else:
        print("The server issued no refresh token: run this again when the sign-in expires.")
    store(orca, args.vault, args.name or urllib.parse.urlsplit(server).hostname, auth)


if __name__ == "__main__":
    main()
