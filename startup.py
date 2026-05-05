#!/usr/bin/env python3
"""从 Vercel DS2API 拉取配置写入 config.json，然后启动 DS2API"""
import json
import os
import sys
import subprocess
import urllib.request

VERCEL_URL = os.environ.get("VERCEL_DS2API_URL", "https://ds2api-deepseek.vercel.app")
VERCEL_ADMIN_KEY = os.environ.get("VERCEL_ADMIN_KEY", "123456789")

def fetch_config():
    """从 Vercel DS2API 拉取完整配置"""
    try:
        # 登录获取 token
        login_req = urllib.request.Request(
            f"{VERCEL_URL}/admin/login",
            data=json.dumps({"admin_key": VERCEL_ADMIN_KEY}).encode(),
            headers={"Content-Type": "application/json"}
        )
        token = json.loads(urllib.request.urlopen(login_req, timeout=10).read())["token"]

        # 获取配置
        config_req = urllib.request.Request(
            f"{VERCEL_URL}/admin/config",
            headers={"Authorization": f"Bearer {token}"}
        )
        config = json.loads(urllib.request.urlopen(config_req, timeout=10).read())

        accounts = config.get("accounts", [])
        keys = config.get("api_keys", [])
        print(f"✅ 从 Vercel 拉取配置: {len(accounts)} 个账号, {len(keys)} 个 API Key")
        return config
    except Exception as e:
        print(f"❌ 从 Vercel 拉取失败: {e}")
        return None

def main():
    # 从 Vercel 拉配置
    config = fetch_config()

    if config:
        with open("/data/config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("✅ 配置已写入 /data/config.json")
    else:
        # 尝试用环境变量兜底
        env_config = os.environ.get("DS2API_CONFIG_JSON")
        if env_config:
            print("⚠️ 使用环境变量 DS2API_CONFIG_JSON 兜底")
            try:
                config = json.loads(env_config)
                with open("/data/config.json", "w") as f:
                    json.dump(config, f, indent=2)
            except:
                print("❌ 环境变量解析失败")

    # 启动 DS2API
    print("🚀 启动 DS2API...")
    proc = subprocess.Popen(["/usr/local/bin/ds2api"])
    proc.wait()

if __name__ == "__main__":
    main()
