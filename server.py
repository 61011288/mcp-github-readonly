import os
import requests
from fastapi import FastAPI, Response
from fastmcp import FastMCP

mcp = FastMCP("github-readonly")

@mcp.tool
def mcp_fetch(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text[:200_000]

# FastAPI 外壳
app = FastAPI()

# 让 RikkaHub 的“GET 探测”通过
@app.get("/mcp")
def mcp_probe():
    # 返回 200 + application/json，避免 406
    return {"status": "ok"}

# 把真正的 MCP handler 挂到同一路径，用 POST 承接
# FastMCP 在 3.x 可以导出 ASGI app：mcp.http_app()（如果你的版本方法名不同，我下面给你兜底）
mcp_asgi = mcp.http_app()  # 如果这里报错，告诉我报错名，我给你换成你版本对应的方法

# 把 ASGI app 挂载到 /mcp （POST/其它方法走 MCP；GET 已经被上面拦截）
app.mount("/mcp", mcp_asgi)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)