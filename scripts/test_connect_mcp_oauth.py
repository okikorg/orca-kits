"""Proves connect_mcp_oauth.py signs in safely and stores exactly the
credential the server accepts (orca-design connected-apps D5.15, test T6).
Each case runs the script against a stub MCP server, authorization server
and Orca API on 127.0.0.1, with a stand-in browser that follows the sign-in
redirect.

    python scripts/test_connect_mcp_oauth.py
"""

import base64
import contextlib
import datetime
import getpass
import hashlib
import http.server
import io
import json
import os
import pathlib
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request

import connect_mcp_oauth as connect

SCRIPT = pathlib.Path(__file__).resolve().parent / "connect_mcp_oauth.py"
# Values that must never reach the terminal or a file.
ORCA_KEY = "orca-key-MARKER-1f3a"
ACCESS = "access-MARKER-7c2e"
REFRESH = "refresh-MARKER-9b4d"
CODE = "code-MARKER-5e8f"
CONFIG_KEY = "config-key-MARKER-2a6c"
PROMPT_KEY = "prompt-key-MARKER-8d1b"
BROWSER = 'import sys, urllib.request\nurllib.request.urlopen(sys.argv[1], timeout=10).read()\n'


class Stub:
    """One loopback server playing the MCP server, its authorization server
    and Orca's API, recording every request."""

    def __init__(self):
        self.role = "admin"
        self.state_override = None
        self.token_error = False
        self.methods = ["S256"]
        self.resource = None  # the protected resource's `resource`; None means the server URL
        self.vaults = []
        self.credentials = {}  # vault id -> list of credentials
        self.requests = []  # (method, path, query, headers, body)
        stub = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                stub.handle(self, "GET")

            def do_POST(self):
                stub.handle(self, "POST")

            def do_DELETE(self):
                stub.handle(self, "DELETE")

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.mcp = f"{self.base}/mcp"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()

    def find(self, method, path):
        return [r for r in self.requests if r[0] == method and r[1] == path]

    def handle(self, h, method):
        url = urllib.parse.urlsplit(h.path)
        length = int(h.headers.get("Content-Length") or 0)
        raw = h.rfile.read(length).decode() if length else ""
        if h.headers.get("Content-Type", "").startswith("application/x-www-form-urlencoded"):
            body = dict(urllib.parse.parse_qsl(raw))
        else:
            body = json.loads(raw) if raw else None
        query = dict(urllib.parse.parse_qsl(url.query))
        self.requests.append((method, url.path, query, dict(h.headers), body))
        status, headers, reply = self.route(method, url.path, query, h.headers, body)
        h.send_response(status)
        for name, value in headers.items():
            h.send_header(name, value)
        data = json.dumps(reply).encode() if reply is not None else b""
        h.send_header("Content-Type", "application/json")
        h.send_header("Content-Length", str(len(data)))
        h.end_headers()
        h.wfile.write(data)

    def route(self, method, path, query, headers, body):
        base = self.base
        if path == "/mcp" and method == "POST":
            return 401, {"WWW-Authenticate": f'Bearer error="unauthorized", resource_metadata="{base}/.well-known/oauth-protected-resource/mcp"'}, None
        if path == "/.well-known/oauth-protected-resource/mcp":
            return 200, {}, {"resource": self.resource or self.mcp, "authorization_servers": [f"{base}/as"]}
        if path == "/.well-known/oauth-authorization-server/as":
            return 200, {}, {
                "issuer": f"{base}/as",
                "authorization_endpoint": f"{base}/as/authorize",
                "token_endpoint": f"{base}/as/token",
                "registration_endpoint": f"{base}/as/register",
                "code_challenge_methods_supported": self.methods,
                "token_endpoint_auth_methods_supported": ["none"],
                "scopes_supported": ["openid", "offline_access"],
            }
        if path == "/as/register":
            return 201, {}, {"client_id": "client-1", "redirect_uris": body["redirect_uris"]}
        if path == "/as/authorize":
            state = self.state_override or query["state"]
            target = query["redirect_uri"] + "?" + urllib.parse.urlencode({"code": CODE, "state": state})
            return 302, {"Location": target}, None
        if path == "/as/token":
            if self.token_error:
                return 400, {}, {"error": "invalid_grant", "error_description": f"bad {CODE} {ACCESS}", "access_token": ACCESS}
            return 200, {}, {"access_token": ACCESS, "token_type": "Bearer", "expires_in": 3600, "refresh_token": REFRESH, "scope": "offline_access"}
        if path == "/api/whoami":
            return 200, {}, {"object": "whoami", "tenant": "org_test", "actor": "user_1", "role": self.role}
        if path == "/v1/vaults" and method == "GET":
            return 200, {}, {"data": self.vaults, "has_more": False}
        if path == "/v1/vaults" and method == "POST":
            vault = {"id": f"vlt_{len(self.vaults) + 1}", "object": "vault", "name": body["name"]}
            self.vaults.append(vault)
            return 200, {}, vault
        parts = path.split("/")
        if len(parts) >= 5 and parts[1:3] == ["v1", "vaults"] and parts[4] == "credentials":
            vault = parts[3]
            rows = self.credentials.setdefault(vault, [])
            if method == "GET":
                return 200, {}, {"data": rows, "has_more": False}
            if method == "POST":
                row = {"id": f"cred_new{len(self.requests)}", "object": "vault.credential", "vault_id": vault, "name": body["name"], "auth": {"type": body["auth"]["type"], "mcp_server_url": body["auth"]["mcp_server_url"]}}
                rows.append(row)
                return 200, {}, row
            if method == "DELETE":
                self.credentials[vault] = [r for r in rows if r["id"] != parts[5]]
                return 200, {}, {"id": parts[5], "deleted": True}
        return 404, {}, {"error": {"message": "not found"}}


def run(stub, *args, env=None, home=None, cwd=None):
    """Run the script as a person would, with the stand-in browser."""
    tools = pathlib.Path(tempfile.mkdtemp())
    (tools / "browser.py").write_text(BROWSER)
    home = home or pathlib.Path(tempfile.mkdtemp())
    environment = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(home),
        "ORCA_API_URL": stub.base,
        "ORCA_API_KEY": ORCA_KEY,
        "BROWSER": f'"{sys.executable}" "{tools / "browser.py"}" %s',
    }
    environment.update(env or {})
    environment = {k: v for k, v in environment.items() if v is not None}
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--server", stub.mcp, "--vault", "apps", *args],
        env=environment,
        cwd=cwd or home,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result


def secrets_in(stub, text):
    verifier = [r[4]["code_verifier"] for r in stub.find("POST", "/as/token")]
    return [s for s in [ORCA_KEY, ACCESS, REFRESH, CODE, CONFIG_KEY, PROMPT_KEY, *verifier] if s in text]


def files_under(folder):
    return sorted(str(p.relative_to(folder)) for p in pathlib.Path(folder).rglob("*"))


def case_pkce_and_state(stub):
    result = run(stub)
    assert result.returncode == 0, result.stderr
    asked = stub.find("GET", "/as/authorize")[0][2]
    sent = stub.find("POST", "/as/token")[0][4]
    assert asked["code_challenge_method"] == "S256", asked
    digest = base64.urlsafe_b64encode(hashlib.sha256(sent["code_verifier"].encode()).digest()).rstrip(b"=").decode()
    assert asked["code_challenge"] == digest, "the challenge is S256 of the verifier the token request sends"
    assert len(asked["state"]) >= 22, "state carries at least 128 bits"
    assert asked["resource"] == stub.mcp and sent["resource"] == stub.mcp, "resource names the MCP server"


def case_wrong_state(stub):
    stub.state_override = "not-the-state"
    result = run(stub)
    assert result.returncode != 0, "a wrong state stops the script"
    assert stub.find("GET", "/as/authorize"), "the sign-in reached the callback"
    assert "state" in result.stderr, result.stderr
    assert not stub.find("POST", "/as/token"), "no token request after a wrong state"
    assert not [r for r in stub.requests if r[0] == "POST" and r[1].endswith("/credentials")], "nothing stored"


def case_loopback_redirect(stub):
    result = run(stub)
    assert result.returncode == 0, result.stderr
    registered = stub.find("POST", "/as/register")[0][4]
    asked = stub.find("GET", "/as/authorize")[0][2]
    uri = urllib.parse.urlsplit(registered["redirect_uris"][0])
    assert (uri.scheme, uri.hostname, uri.path) == ("http", "127.0.0.1", "/callback"), registered
    assert asked["redirect_uri"] == registered["redirect_uris"][0]
    assert registered["token_endpoint_auth_method"] == "none", "a public client"
    listener = connect.Callback()
    try:
        assert listener.server.server_address[0] == "127.0.0.1", "the listener binds loopback only"
    finally:
        listener.close()


def callback(port, query):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/callback?{urllib.parse.urlencode(query)}", timeout=5) as reply:
            return reply.status
    except urllib.error.HTTPError as error:
        return error.code


def refused(port):
    with contextlib.closing(socket.socket()) as s:
        s.settimeout(2)
        return s.connect_ex(("127.0.0.1", port)) != 0


def case_one_callback(stub):
    listener = connect.Callback()
    port = listener.port
    listener.start()
    status = callback(port, {"code": CODE, "state": "s1"})
    code = listener.wait("s1", timeout=5)
    assert status == 200 and code == CODE
    assert refused(port), "after one callback the port is closed"
    listener = connect.Callback()
    port = listener.port
    listener.start()
    started = time.monotonic()
    try:
        listener.wait("s1", timeout=0.5)
        raise AssertionError("a wait with no callback ends in an exit")
    except SystemExit:
        pass
    assert time.monotonic() - started < 5
    assert refused(port), "after a timeout the port is closed"


def case_key_never_an_argument(stub):
    flags = [flag for flag in connect.build_parser()._option_string_actions if flag.startswith("--")]
    assert not [f for f in flags if "key" in f or "token" in f or "secret" in f], flags
    result = run(stub, "--api-key", ORCA_KEY)
    assert result.returncode == 2 and "unrecognized arguments" in result.stderr
    assert not stub.requests, "an argument key reaches nothing"
    # The environment first.
    result = run(stub)
    assert result.returncode == 0, result.stderr
    assert stub.find("GET", "/api/whoami")[-1][3]["Authorization"] == f"Bearer {ORCA_KEY}"
    # Then the CLI's store, as orca-cli resolves it.
    config = pathlib.Path(tempfile.mkdtemp())
    (config / "config.json").write_text(json.dumps({"currentContext": "work", "contexts": {"work": {"apiUrl": stub.base, "apiKey": CONFIG_KEY}}}))
    result = run(stub, env={"ORCA_API_KEY": None, "ORCA_API_URL": None, "ORCA_CONFIG_DIR": str(config)})
    assert result.returncode == 0, result.stderr
    assert stub.find("GET", "/api/whoami")[-1][3]["Authorization"] == f"Bearer {CONFIG_KEY}"
    assert not secrets_in(stub, result.stdout + result.stderr)
    # Then a hidden prompt.
    saved = dict(os.environ)
    asked = []
    original = getpass.getpass
    try:
        os.environ.pop("ORCA_API_KEY", None)
        os.environ["ORCA_API_URL"] = stub.base
        os.environ["ORCA_CONFIG_DIR"] = tempfile.mkdtemp()
        getpass.getpass = lambda prompt="": asked.append(prompt) or PROMPT_KEY
        assert connect.orca_target() == (stub.base, PROMPT_KEY)
        assert asked, "the key comes from getpass, which hides it"
    finally:
        getpass.getpass = original
        os.environ.clear()
        os.environ.update(saved)


def case_nothing_secret_printed_or_written(stub):
    home = pathlib.Path(tempfile.mkdtemp())
    before = files_under(home)
    result = run(stub, home=home)
    assert result.returncode == 0, result.stderr
    leaked = secrets_in(stub, result.stdout + result.stderr)
    assert not leaked, f"printed: {leaked}"
    assert files_under(home) == before, "the script writes no file"
    stub.requests.clear()
    stub.token_error = True
    result = run(stub, home=home)
    assert result.returncode != 0
    assert "invalid_grant" in result.stderr, "the error code is shown"
    leaked = secrets_in(stub, result.stdout + result.stderr)
    assert not leaked, f"a token endpoint error printed: {leaked}"
    assert files_under(home) == before


def case_credential_body(stub):
    result = run(stub, "--name", "apps-connect")
    assert result.returncode == 0, result.stderr
    assert stub.find("POST", "/v1/vaults")[0][4] == {"name": "apps"}
    body = [r for r in stub.requests if r[0] == "POST" and r[1].endswith("/credentials")][0][4]
    expires = body["auth"].pop("expires_at")
    assert body == {
        "name": "apps-connect",
        "auth": {
            "type": "mcp_oauth",
            "mcp_server_url": stub.mcp,
            "access_token": ACCESS,
            "refresh": {
                "client_id": "client-1",
                "refresh_token": REFRESH,
                "token_endpoint": f"{stub.base}/as/token",
                "token_endpoint_auth": {"type": "none"},
                "resource": stub.mcp,
                "scope": "offline_access",
            },
        },
    }, body
    left = datetime.datetime.fromisoformat(expires.replace("Z", "+00:00")) - datetime.datetime.now(datetime.timezone.utc)
    assert 3500 < left.total_seconds() <= 3600, expires
    assert "vlt_1" in result.stdout and "cred_" in result.stdout, "the ids are shown"


def case_member_key_stops(stub):
    stub.role = "member"
    result = run(stub)
    assert result.returncode != 0
    assert "admin" in result.stderr
    assert not stub.find("POST", "/as/register") and not stub.find("GET", "/as/authorize"), "it stops before signing in"


def case_rerun_replaces_in_the_named_vault(stub):
    stub.vaults = [{"id": "vlt_a", "name": "apps"}, {"id": "vlt_b", "name": "other"}]
    stub.credentials = {
        "vlt_a": [
            {"id": "cred_old", "name": "old", "auth": {"type": "mcp_oauth", "mcp_server_url": stub.mcp}},
            {"id": "cred_keep", "name": "keep", "auth": {"type": "static_bearer", "mcp_server_url": "https://elsewhere.example/mcp"}},
        ],
        "vlt_b": [{"id": "cred_b", "name": "b", "auth": {"type": "mcp_oauth", "mcp_server_url": stub.mcp}}],
    }
    result = run(stub)
    assert result.returncode == 0, result.stderr
    writes = [(r[0], r[1]) for r in stub.requests if r[0] in ("POST", "DELETE") and "/v1/vaults/" in r[1]]
    assert writes == [("POST", "/v1/vaults/vlt_a/credentials"), ("DELETE", "/v1/vaults/vlt_a/credentials/cred_old")], writes
    assert "cred_old" in result.stdout, "the replaced credential's id is shown"
    assert [r["id"] for r in stub.credentials["vlt_b"]] == ["cred_b"], "other vaults are untouched"
    assert not stub.find("POST", "/v1/vaults"), "the named vault is reused"


def case_discovery_refusals(stub):
    stub.methods = ["plain"]
    result = run(stub)
    assert result.returncode != 0 and "S256" in result.stderr
    assert not stub.find("POST", "/as/register")
    stub.methods = ["S256"]
    stub.resource = "https://another.example/mcp"
    result = run(stub)
    assert result.returncode != 0, "a protected resource naming another server stops it"
    assert not stub.find("POST", "/as/register")


CASES = [
    case_pkce_and_state,
    case_wrong_state,
    case_loopback_redirect,
    case_one_callback,
    case_key_never_an_argument,
    case_nothing_secret_printed_or_written,
    case_credential_body,
    case_member_key_stops,
    case_rerun_replaces_in_the_named_vault,
    case_discovery_refusals,
]


def main():
    failures = []
    for case in CASES:
        stub = Stub()
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                case(stub)
        except Exception as error:  # every failure is reported, then the run fails
            failures.append(f"{case.__name__}: {type(error).__name__}: {error}")
        finally:
            stub.close()
    for failure in failures:
        print(failure, file=sys.stderr)
    if failures:
        sys.exit(1)
    print(f"ok, {len(CASES)} cases")


if __name__ == "__main__":
    main()
