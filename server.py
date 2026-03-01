import os
import requests
from fastmcp import FastMCP

mcp = FastMCP("github-sse")

@mcp.tool
def mcp_ping() -> str:
    print("[mcp_ping] called", flush=True)
    return "pong"

@mcp.tool
def mcp_fetch(url: str) -> str:
    print(f"[mcp_fetch] called with url={url}", flush=True)
    try:
        r = requests.get(url, timeout=30)
        print(f"[mcp_fetch] status={r.status_code}", flush=True)
        r.raise_for_status()
        text = r.text[:200_000]
        print(f"[mcp_fetch] returning {len(text)} chars", flush=True)
        return text
    except Exception as e:
        print(f"[mcp_fetch] ERROR: {repr(e)}", flush=True)
        raise

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=port,
        path="/sse",
    )