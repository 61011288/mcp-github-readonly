import os
import requests
from fastmcp import FastMCP

mcp = FastMCP("github-readonly")

@mcp.tool
def mcp_fetch(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text[:200_000]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        # mount_path="/mcp",  # 删掉
    )