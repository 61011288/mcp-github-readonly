import os
import requests
from fastmcp import FastMCP

mcp = FastMCP("github-sse")

@mcp.tool
def ping_star() -> str:
    print("[ping_star] called", flush=True)
    return "pong"

@mcp.tool
def read_url_text(url: str) -> str:
    print(f"[read_url_text] called with url={url}", flush=True)
    try:
        r = requests.get(url, timeout=30)
        print(f"[read_url_text] status={r.status_code}", flush=True)
        r.raise_for_status()
        text = r.text[:200_000]
        print(f"[read_url_text] returning {len(text)} chars", flush=True)
        return text
    except Exception as e:
        print(f"[read_url_text] ERROR: {repr(e)}", flush=True)
        raise

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=port,
        path="/sse",
    )