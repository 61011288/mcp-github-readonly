from fastmcp import FastMCP
import requests

mcp = FastMCP("github-readonly")

@mcp.tool
def mcp_fetch(url: str) -> str:
    """Fetch a URL and return text content (read-only)."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    # 控制一下体积，避免移动端渲染/传输炸
    text = r.text
    return text[:200_000]

if __name__ == "__main__":
    # 关键：streamable-http + 挂载路径 /mcp
    mcp.run(transport="streamable-http", host="0.0.0.0", port=10000, mount_path="/mcp")