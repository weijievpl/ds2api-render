#!/usr/bin/env python3
"""从 MongoDB 拉取配置写入 config.json，然后启动 DS2API"""
import json
import os
import sys
import subprocess
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "")
DB_NAME = "ds2api"
COLLECTION = "config"

def fetch_config():
    if not MONGO_URI:
        print("⚠️ MONGO_URI 未设置，跳过 MongoDB")
        return None
    
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        col = db[COLLECTION]
        doc = col.find_one({"_id": "main"})
        client.close()
        if doc:
            config = doc.get("config", {})
            print(f"✅ 从 MongoDB 拉取配置: {len(config.get('accounts', []))} 个账号")
            return config
        else:
            print("⚠️ MongoDB 中没有配置")
            return None
    except Exception as e:
        print(f"❌ MongoDB 连接失败: {e}")
        return None

def push_config(config):
    """把配置推到 MongoDB"""
    if not MONGO_URI:
        return
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        col = db[COLLECTION]
        col.update_one({"_id": "main"}, {"$set": {"config": config}}, upsert=True)
        client.close()
        print("✅ 配置已推到 MongoDB")
    except Exception as e:
        print(f"❌ 推送 MongoDB 失败: {e}")

def main():
    # 从 MongoDB 拉配置
    config = fetch_config()
    
    if config:
        with open("/app/data/config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("✅ 配置已写入 /app/data/config.json")
    
    # 启动 DS2API
    print("🚀 启动 DS2API...")
    proc = subprocess.Popen(["/usr/local/bin/ds2api"])
    proc.wait()

if __name__ == "__main__":
    main()
