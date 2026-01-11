import aiohttp
import asyncio
import random
import time
import uuid
import string
import hashlib
import base64
import json
import re
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # السماح لأي متصفح بالوصول

ua_gen = None
try:
    import fake_useragent
    ua_gen = fake_useragent.FakeUserAgent()
except:
    ua_gen = None

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

async def pu(username):
    try:
        ii = rn(19)
        di = rn(19)
        cd = ru()
        ou = rh(16)
        sn = set()
        au = []
        pt = ""
        mt = ""
        tc = 0

        ts = int(time.time())
        ua = ra()
        headers = {
            'User-Agent': ua,
            'Accept-Encoding': "gzip",
            'x-ss-dp': "1340",
            'x-tt-req-timeout': "90000",
            'sdk-version': "2",
            'x-tt-token': rh(96),
            'passport-sdk-version': "30990",
            'x-tt-ultra-lite': "1",
            'x-vc-bdturing-sdk-version': "2.3.2.i18n",
            'x-tt-store-region': "iq",
            'x-tt-store-region-src': "uid",
            'x-ladon': rh(64),
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

        url = f"https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/following/list/?" \
              f"user_id={username}&count=200&page_token={pt}&max_time={mt}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                rs = await resp.json()
                us = [item['unique_id'] for item in rs.get('followings', [])]
                return us
    except Exception as e:
        return {"error": str(e)}

@app.route("/pull_followings", methods=["GET"])
def pull_followings():
    username = request.args.get("username")
    if not username:
        return jsonify({"status": "failed", "message": "No username provided"}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    users = loop.run_until_complete(pu(username))
    loop.close()

    return jsonify({"status": "success", "username": username, "followings": users})

@app.route("/", methods=["GET"])
def home():
    return "🚀 TikTok Scraper API is Running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
