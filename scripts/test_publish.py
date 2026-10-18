"""Proves publish.py only updates drafts: it never calls the API's publish,
sends no author, and prints the operator line. Each case runs publish.py on a
copy of kits/scout with every request faked, git included, so nothing reaches
a server.

    python scripts/test_publish.py
"""

import contextlib
import io
import json
import os
import pathlib
import shutil
import sys
import tempfile
import types
import urllib.request

import openai

import kitlib
import publish

SCOUT = kitlib.KITS / "scout"
KIT = "kit_f61441ef49104825b8b92b21c9a6e489"
PUBLIC_ID = "kit-tdCEUXGA3NbuIWJJ6"


class Client:
    """Stands in for OpenAI(): every call is recorded, and returns an id."""

    def __init__(self, calls, path=()):
        self.calls, self.path = calls, path

    def __getattr__(self, name):
        return Client(self.calls, self.path + (name,))

    def __call__(self, *args, **body):
        self.calls.append((".".join(self.path), body))
        return types.SimpleNamespace(id="agent_new", version=1)


class Response(io.BytesIO):
    headers = {}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def run(published, argv):
    """publish.main on a copy of Scout with published.json as given: the
    output, the kit API's requests as (method, path, body), and the exit."""
    requests, calls = [], []

    def urlopen(request, timeout=None):
        body = json.loads(request.data) if request.data else None
        requests.append((request.get_method(), request.full_url.removeprefix("http://orca.test"), body))
        return Response(json.dumps({"id": "kit_new"}).encode())

    def git(*args, check=True):
        return "0123456789abcdef" if args[0] == "rev-parse" else ""

    on_main = types.SimpleNamespace(run=lambda *a, **k: types.SimpleNamespace(returncode=0))
    with tempfile.TemporaryDirectory(dir=kitlib.ROOT, prefix=".test-") as tmp:
        kits = pathlib.Path(tmp)
        shutil.copytree(SCOUT, kits / "scout", ignore=shutil.ignore_patterns("published.json", "__pycache__"))
        (kits / "scout" / "published.json").write_text(json.dumps(published))
        saved = (kitlib.KITS, kitlib.git, publish.subprocess, urllib.request.urlopen, openai.OpenAI, dict(os.environ))
        kitlib.KITS, kitlib.git, publish.subprocess = kits, git, on_main
        urllib.request.urlopen = urlopen
        openai.OpenAI = lambda **_: Client(calls)
        os.environ.update(ORCA_KITS_API_KEY="test-key", ORCA_ORIGIN="http://orca.test")
        out, code = io.StringIO(), 0
        try:
            with contextlib.redirect_stdout(out):
                publish.main(argv)
        except SystemExit as error:
            code = error.code
        finally:
            kitlib.KITS, kitlib.git, publish.subprocess, urllib.request.urlopen, openai.OpenAI, env = saved
            os.environ.clear()
            os.environ.update(env)
        return out.getvalue(), requests, code


def main():
    failures = []

    def expect(name, ok, detail):
        if ok:
            print(f"ok: {name}")
        else:
            failures.append(f"{name}: {detail}")

    out, requests, code = run({"agent": "agent_1", "kit": KIT, "public_id": PUBLIC_ID}, ["scout"])
    paths = [path for _, path, _ in requests]
    expect("a published kit's draft is updated", code == 0 and ("PATCH", f"/api/kits/{KIT}") in [r[:2] for r in requests], (code, requests))
    expect("it never calls publish", not any(p.endswith("/publish") for p in paths), paths)
    expect("it sends no author", all("author" not in (body or {}) for _, _, body in requests), requests)
    line = f"orca-agent-server kits publish --kit {KIT} --public-id {PUBLIC_ID}"
    expect("it prints the operator line with the public id", line in out.splitlines(), out)

    out, requests, code = run({"agent": "agent_1"}, ["scout", "--allow-new"])
    paths = [path for _, path, _ in requests]
    expect("a new kit's draft is created", code == 0 and [r[:2] for r in requests] == [("POST", "/api/kits")], (code, requests))
    expect("a new kit is never published", not any(p.endswith("/publish") for p in paths), paths)
    expect("a first publish's line has no --public-id", "orca-agent-server kits publish --kit kit_new" in out.splitlines(), out)

    out, requests, code = run({"agent": "agent_1", "kit": KIT, "public_id": PUBLIC_ID}, ["scout", "--draft"])
    expect("--draft is gone", code == publish.__doc__ and not requests, (code, requests))

    for failure in failures:
        print(failure, file=sys.stderr)
    if failures:
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main()
