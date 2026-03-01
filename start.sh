#!/usr/bin/env bash
set -e

# 说明：
# - mcp-proxy 在“SSE to stdio”模式下运行：对外开 SSE 服务，对内拉起 stdio 的 fetch server
# - 监听 0.0.0.0:$PORT，才能让 Render 的公网访问到
# - 默认 SSE endpoint 是 /sse（mcp-proxy 文档示例就是 http://host:port/sse）
#   :contentReference[oaicite:3]{index=3}

mcp-proxy --host 0.0.0.0 --port "${PORT}" --pass-environment -- \
  uvx mcp-server-fetch