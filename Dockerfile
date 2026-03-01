FROM python:3.11-slim

# 基础依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# 安装 mcp-proxy + fetch server + uv（uv 用来更稳地跑 mcp-server-fetch）
RUN pip install --no-cache-dir mcp-proxy mcp-server-fetch uv

# 拷贝启动脚本
WORKDIR /app
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENV PORT=8080
EXPOSE 8080

CMD ["/app/start.sh"]