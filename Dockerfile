FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl tar \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 下载预编译二进制（包含静态文件）
RUN curl -sL "https://github.com/CJackHwang/ds2api/releases/download/v4.4.2/ds2api_v4.4.2_linux_amd64.tar.gz" -o /tmp/ds2api.tar.gz \
    && tar -xzf /tmp/ds2api.tar.gz -C /tmp \
    && cp /tmp/ds2api_v4.4.2_linux_amd64/ds2api /usr/local/bin/ds2api \
    && chmod +x /usr/local/bin/ds2api \
    && mkdir -p /app/static \
    && cp -r /tmp/ds2api_v4.4.2_linux_amd64/static/* /app/static/ \
    && rm -rf /tmp/ds2api*

# 创建数据目录和默认配置
RUN mkdir -p /app/data /data && chmod 777 /app/data /data \
    && echo '{"accounts":[],"api_keys":[]}' > /data/config.json

EXPOSE 10000

CMD ["ds2api"]
