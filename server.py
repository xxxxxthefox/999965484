import aiohttp
import asyncio
import random
import time
import uuid
import string
import hashlib
import base64
import json
import ms4
import re
import fake_useragent
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ua_gen = fake_useragent.FakeUserAgent()

def rn(l=10):
    return ''.join(random.choice(string.digits) for _ in range(l))

def rh(l=32):
    return ''.join(random.choice('0123456789abcdef') for _ in range(l))

def ru():
    return str(uuid.uuid4())

def ra():
    br = ["Infinix", "Samsung", "Xiaomi", "Huawei", "Realme", "Oppo", "Vivo", "Tecno"]
    mo = ["X692", "A52", "M21", "Note9", "Y20", "C25", "F17", "P30"]
    av = ["10", "11", "12", "13"]
    bv = ["QP1A.190711.020", "RP1A.200720.011", "TP1A.220905.001", "SP1A.210812.016"]
    return f"com.zhiliaoapp.musically.go/370402 (Linux; U; Android {random.choice(av)}; ar; {random.choice(br)} {random.choice(mo)}; Build/{random.choice(bv)}; tt-ok/3.12.13.27-ul)"

def gx(ts):
    b = hashlib.md5(str(ts).encode()).hexdigest()
    return "8404" + b[:30]

def ga(ts, di, ii):
    r = f"{di}:{ii}:{ts}"
    h = hashlib.sha256(r.encode()).digest()
    return base64.b64encode(h).decode()

def gp(pd):
    e = json.dumps(pd, separators=(',', ':')).encode()
    return base64.b64encode(e).decode()

async def pull_followings(username):
    info = ms4.InfoTik.TikTok_Info(username)
    user_id = info["id"]

    async with aiohttp.ClientSession() as s:
        async with s.get(f'https://www.tiktok.com/@{username}', headers={'User-Agent': ua_gen.random}) as r:
            html = await r.text()

    sec_uid = re.search(r'"secUid":"([^"]+)"', html).group(1)

    ii = rn(19)
    di = rn(19)
    cd = ru()
    ou = rh(16)
    pt = ""
    mt = ""
    all_users = []
    seen = set()

    while True:
        ts = int(time.time())
        headers = {
            'User-Agent': ra(),
            'x-khronos': str(ts),
            'x-argus': ga(ts, di, ii),
            'x-gorgon': gx(ts),
            'X-Tt-Params': gp({
                "iid": ii,
                "device_id": di,
                "cdid": cd,
                "ts": ts,
                "version": "37.4.2",
                "region": "IQ"
            }),
            'Cookie': f"install_id={ii}; device_id={di}; odin_tt={rh(64)}; sessionid={rh(32)}"
        }

        url = f"https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/following/list/?user_id={user_id}&sec_user_id={sec_uid}&count=200&page_token={pt}&max_time={mt}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                data = await resp.json()

        users = [u["unique_id"] for u in data.get("followings", [])]
        for u in users:
            if u not in seen:
                seen.add(u)
                all_users.append(u)

        if not data.get("has_more"):
            break

        pt = data.get("next_page_token", "")
        mt = data.get("min_time", "")

    return all_users

@app.route("/pull_followings", methods=["GET"])
def api_pull():
    username = request.args.get("username")
    if not username:
        return jsonify({"status": "error", "message": "username required"}), 400

    result = asyncio.run(pull_followings(username))
    return jsonify({
        "status": "success",
        "username": username,
        "count": len(result),
        "followings": result
    })

@app.route("/")
def home():
    return "🚀 TikTok Followings API Running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
