import os
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastmcp import FastMCP

mcp = FastMCP("github-readonly")

@mcp.tool
def mcp_fetch(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text[:200_000]

# 真正的 MCP ASGI app，挂在 /mcp
mcp_app = mcp.http_app(path="/mcp")

# 外层 FastAPI
app = FastAPI(lifespan=mcp_app.lifespan)

# 给 RikkaHub 的 GET 探测一个 200，避免它因为 406 直接放弃
@app.get("/mcp")
async def mcp_probe():
    return JSONResponse({"status": "ok"})

# 真正的 MCP 走 /mcp/...
app.mount("/", mcp_app)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)