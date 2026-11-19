"""Tiny stdio MCP client for Native's mcp-stdio binary (newline-delimited JSON-RPC)."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "vendor/native/target/debug/mcp-stdio"


def _find(obj, key):
    if isinstance(obj, dict):
        if key in obj and isinstance(obj[key], str):
            return obj[key]
        for v in obj.values():
            r = _find(v, key)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = _find(v, key)
            if r:
                return r
    return None


class Native:
    def __init__(self, db):
        self.p = subprocess.Popen([str(BIN), str(db)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, text=True, bufsize=1)
        self.n = 0
        self.req("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                "clientInfo": {"name": "bench-loader", "version": "0.1"}})
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")

    def req(self, method, params=None):
        self.n += 1
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params or {}}) + "\n")
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError("mcp-stdio exited: " + self.p.stderr.read()[-2000:])
            msg = json.loads(line)
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise RuntimeError(json.dumps(msg["error"])[:2000])
                return msg["result"]

    def call(self, tool, args):
        r = self.req("tools/call", {"name": tool, "arguments": args})
        if r.get("isError"):
            raise RuntimeError(f"{tool}: " + json.dumps(r.get("structuredContent") or r.get("content"))[:2000])
        return r.get("structuredContent") or r

    def op(self, executor, operation, arguments=None, **envelope):
        """Call one operation through Native's executor surface."""
        args = {"operation": operation, "arguments": arguments or {}, "format": "json", **envelope}
        if getattr(self, "run_key", None):
            args.setdefault("run_key", self.run_key)
        direct = {"records_read": {"get_record", "search"}}
        if executor in ("system_read", "guidance_read", "records_write", "records_lifecycle",
                        "coordination_write", "sql_read") or operation in direct.get(executor, ()):
            return self.call(executor, args)
        return self.call("call_executor", {"executor": executor, **args})

    def bootstrap(self):
        r = self.call("bootstrap", {"format": "json"})
        self.run_key = _find(r, "run_key")
        return r

    def close(self):
        self.p.stdin.close()
        self.p.wait(timeout=10)
