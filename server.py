import os
import requests
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastmcp import FastMCP

mcp = FastMCP("github-readonly")

@mcp.tool
def mcp_fetch(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text[:200_000]

# 关键：
# 让 FastMCP 认为自己的 HTTP 入口在 "/"，
# 然后我们把它整体 mount 到 "/mcp"
mcp_app = mcp.http_app(path="/")

app = FastAPI(lifespan=mcp_app.lifespan)

# 让 RikkaHub 的探测通过
@app.api_route("/mcp", methods=["GET", "HEAD"])
async def mcp_probe():
    return JSONResponse({"status": "ok"})

# 真正的 MCP 处理
app.mount("/mcp", mcp_app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)