#!/usr/bin/env python3
"""Connect Apollo's MCP server to an Orca vault with OAuth, for the Apollo GTM
Agent and Demo Prep Agent kits.

1. Registers an OAuth client with Apollo (dynamic client registration).
2. Opens your browser so you can approve access to your Apollo account.
3. Calls three free Apollo tools to prove the granted scopes work.
4. Stores the access and refresh tokens as an `mcp_oauth` credential in an
   Orca vault. Orca refreshes the token itself; the model never sees it.

The scopes are read-only (search, enrich and read), so the token cannot send
email or change anything in Apollo. Tokens are never printed or written to
disk. The Orca API key comes from ORCA_API_KEY, or else from the orca CLI's
config (run `orca login` first); either must be an admin's.

Usage: python3 connect_apollo.py [--vault apollo] [--port 8765]
"""

import argparse
import base64
import hashlib
import http.server
import json
import os
import pathlib
import secrets
import ssl
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime, timedelta, timezone

MCP_URL = "https://mcp.apollo.io/mcp"
AUTH_METADATA_URL = "https://mcp.apollo.io/.well-known/oauth-authorization-server"
USER_AGENT = "orca-kits-apollo/1.0"


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


SSL_CONTEXT = ssl_context()

# Read-only scopes: search, enrich and read. No sequence, send, CRM-write or
# purchase scopes, so the token cannot send email even if the agent tried.
DEFAULT_SCOPES = " ".join([
    "read_user_profile",
    "organizations_enrich",
    "organizations_bulk_enrich",
    "organizations_search",
    "mixed_companies_search",
    "organizations_job_posting",
    "mixed_people_api_search",
    "people_match",
    "people_bulk_match",
    "contacts_search",
    "contact_read",
])


def request_json(url, body=None, headers=None, form=False, method=None):
    headers = dict(headers or {})
    data = None
    if body is not None:
        if form:
            data = urllib.parse.urlencode(body).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
    headers.setdefault("Accept", "application/json")
    # Apollo's Cloudflare rejects urllib's default User-Agent (error 1010).
    headers.setdefault("User-Agent", USER_AGENT)
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60, context=SSL_CONTEXT) as resp:
            raw = resp.read().decode()
            return resp.status, resp.headers, raw
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read().decode()


def orca_context():
    """(base URL ending in /v1, API key), from the environment or the orca CLI."""
    if os.environ.get("ORCA_API_KEY"):
        base_url = os.environ.get("ORCA_BASE_URL", "https://api.orcapods.ai/v1")
        return base_url.rstrip("/"), os.environ["ORCA_API_KEY"]
    config = json.loads((pathlib.Path.home() / ".config/orca/config.json").read_text())
    ctx = config["contexts"][config["currentContext"]]
    return ctx["apiUrl"].rstrip("/") + "/v1", ctx["apiKey"]


def orca(method, path, body=None):
    base_url, api_key = orca_context()
    status, _, raw = request_json(
        f"{base_url}{path}", body, {"Authorization": f"Bearer {api_key}"}, method=method
    )
    if status >= 400:
        sys.exit(f"Orca {method} {path} failed: {status} {raw[:500]}")
    return json.loads(raw) if raw else {}


def wait_for_code(port, state, timeout_s=600):
    """Accept exactly one OAuth redirect on 127.0.0.1, then stop listening."""
    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if "code" not in query and "error" not in query:
                self.send_response(404)
                self.end_headers()
                return
            result.update({k: v[0] for k, v in query.items()})
            ok = "code" in query and query.get("state", [""])[0] == state
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            message = "Apollo connected. You can close this tab." if ok else "Apollo authorization failed. Check the terminal."
            self.wfile.write(f"<p>{message}</p>".encode())
            threading.Thread(target=self.server.shutdown, daemon=True).start()

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    timer = threading.Timer(timeout_s, server.shutdown)
    timer.start()
    server.serve_forever()
    timer.cancel()
    server.server_close()

    if "error" in result:
        sys.exit(f"Apollo refused authorization: {result.get('error')} {result.get('error_description', '')}")
    if "code" not in result:
        sys.exit("Timed out waiting for Apollo authorization.")
    if result.get("state") != state:
        sys.exit("OAuth state mismatch; aborting.")
    return result["code"]


def mcp_post(access_token, payload, session_id=None):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    status, resp_headers, raw = request_json(MCP_URL, payload, headers)
    if status >= 400:
        sys.exit(f"Apollo MCP {payload.get('method')} failed: {status} {raw[:500]}")
    # Streamable HTTP may answer with an SSE stream; take the last data line.
    if raw.lstrip().startswith("event:") or raw.lstrip().startswith("data:"):
        data_lines = [line[5:].strip() for line in raw.splitlines() if line.startswith("data:")]
        raw = data_lines[-1] if data_lines else "{}"
    return resp_headers.get("Mcp-Session-Id") or session_id, (json.loads(raw) if raw.strip() else {})


def list_mcp_tools(access_token):
    session_id, init = mcp_post(access_token, {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "orca-kits-apollo", "version": "1.0"},
        },
    })
    mcp_post(access_token, {"jsonrpc": "2.0", "method": "notifications/initialized"}, session_id)
    tools, cursor = [], None
    while True:
        params = {"cursor": cursor} if cursor else {}
        _, page = mcp_post(access_token, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": params}, session_id)
        result = page.get("result", {})
        tools.extend(result.get("tools", []))
        cursor = result.get("nextCursor")
        if not cursor:
            return init.get("result", {}).get("serverInfo", {}), tools, session_id


# Free calls (0 credits) that prove the granted scopes cover the agent's tools.
SMOKE_TESTS = [
    ("apollo_organizations_lookup", {"q_organization_fuzzy_name": "apollo.io", "per_page": 1}),
    ("apollo_mixed_people_api_search", {"q_organization_domains_list": ["apollo.io"], "per_page": 1}),
    ("apollo_users_api_profile", {"include_credit_usage": False}),
]


def smoke_test(access_token, session_id):
    failures = []
    for name, arguments in SMOKE_TESTS:
        _, reply = mcp_post(access_token, {
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        }, session_id)
        result = reply.get("result", {})
        if "error" in reply or result.get("isError"):
            text = " ".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")
            failures.append(f"{name}: {reply.get('error') or text[:300]}")
        else:
            print(f"Smoke test passed: {name}")
    if failures:
        sys.exit("Apollo tool calls failed with this token; nothing was stored.\n" + "\n".join(failures))


def upsert_vault_credential(vault_name, auth):
    vaults = orca("GET", "/vaults?limit=100").get("data", [])
    vault = next((v for v in vaults if v.get("name") == vault_name), None)
    if vault is None:
        vault = orca("POST", "/vaults", {"name": vault_name})
        print(f"Created Orca vault {vault_name!r} ({vault['id']}).")
    # Each run registers a new OAuth client, and rotation cannot change the
    # client_id, so replace any older credential for this server outright.
    creds = orca("GET", f"/vaults/{vault['id']}/credentials?limit=100").get("data", [])
    for old in creds:
        if old.get("auth", {}).get("mcp_server_url") == MCP_URL:
            orca("DELETE", f"/vaults/{vault['id']}/credentials/{old['id']}")
            print(f"Replaced old credential {old['name']!r} ({old['id']}).")
    cred = orca("POST", f"/vaults/{vault['id']}/credentials", {"name": "apollo-mcp", "auth": auth})
    print(f"Added credential 'apollo-mcp' ({cred['id']}) to vault {vault_name!r} ({vault['id']}).")
    return vault["id"]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="apollo", help="Orca vault name (default: apollo)")
    parser.add_argument("--port", type=int, default=8765, help="local port for the OAuth redirect")
    parser.add_argument("--scopes", default=DEFAULT_SCOPES, help="space-separated Apollo OAuth scopes")
    args = parser.parse_args()

    status, _, raw = request_json(AUTH_METADATA_URL)
    if status >= 400:
        sys.exit(f"Could not read Apollo's OAuth metadata: {status} {raw[:300]}")
    meta = json.loads(raw)
    redirect_uri = f"http://127.0.0.1:{args.port}/callback"

    status, _, raw = request_json(meta["registration_endpoint"], {
        "client_name": "Orca Apollo kits",
        "redirect_uris": [redirect_uri],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
        "scope": args.scopes,
    })
    if status >= 400:
        sys.exit(f"Apollo client registration failed: {status} {raw[:500]}")
    client = json.loads(raw)
    client_id = client["client_id"]
    client_secret = client.get("client_secret")

    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(24)
    authorize_url = meta["authorization_endpoint"] + "?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": args.scopes,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "resource": MCP_URL,
    })

    print("Approve Apollo access in your browser. If it did not open, visit:\n")
    print(authorize_url + "\n", flush=True)
    webbrowser.open(authorize_url)
    code = wait_for_code(args.port, state)

    token_body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "code_verifier": verifier,
        "resource": MCP_URL,
    }
    if client_secret:
        token_body["client_secret"] = client_secret
    status, _, raw = request_json(meta["token_endpoint"], token_body, form=True)
    if status >= 400:
        sys.exit(f"Apollo token exchange failed: {status} {raw[:300]}")
    tokens = json.loads(raw)
    granted_scope = tokens.get("scope", args.scopes)

    server_info, tools, session_id = list_mcp_tools(tokens["access_token"])
    print(f"Apollo MCP ({server_info.get('name', 'unknown')}) offers {len(tools)} tools.")
    smoke_test(tokens["access_token"], session_id)

    auth = {"type": "mcp_oauth", "mcp_server_url": MCP_URL, "access_token": tokens["access_token"]}
    if tokens.get("expires_in"):
        expires = datetime.now(timezone.utc) + timedelta(seconds=int(tokens["expires_in"]))
        auth["expires_at"] = expires.strftime("%Y-%m-%dT%H:%M:%SZ")
    if tokens.get("refresh_token"):
        endpoint_auth = (
            {"type": "client_secret_post", "client_secret": client_secret}
            if client_secret else {"type": "none"}
        )
        auth["refresh"] = {
            "client_id": client_id,
            "refresh_token": tokens["refresh_token"],
            "token_endpoint": meta["token_endpoint"],
            "token_endpoint_auth": endpoint_auth,
            "resource": MCP_URL,
            "scope": granted_scope,
        }
    else:
        print("Apollo issued no refresh token; rerun this script when the access token expires.")

    upsert_vault_credential(args.vault, auth)


if __name__ == "__main__":
    main()
