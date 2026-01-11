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

# ----- إعداد Flask -----
app = Flask(__name__)
CORS(app)

# ----- توليد User-Agent -----
ua_gen = None
try:
    ua_gen = fake_useragent.FakeUserAgent()
except:
    ua_gen = None

# ----- دوال مساعدة -----
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

# ----- دالة لجلب Followings -----
async def get_followings(username):
    try:
        m = ms4.InfoTik.TikTok_Info(username)
        ui_ = m["id"]
        up = f'https://www.tiktok.com/@{username}'

        async with aiohttp.ClientSession() as s:
            async with s.get(up, headers={'User-Agent': ua_gen.random if ua_gen else ra()}) as r:
                rt = await r.text()

        su = re.search(r'"secUid":"([^"]+)"', rt).group(1)
        ii = rn(19)
        di = rn(19)
        cd = ru()
        ou = rh(16)
        sn = set()
        au = []
        pt = ""
        mt = ""

        while True:
            ts = int(time.time())
            ua = ra()
            hd = {
                'User-Agent': ua,
                'Accept-Encoding': "gzip",
                'rpc-persist-pyxis-policy-v-tnc': "1",
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
                'X-Tt-Params': gp({"iid": ii, "device_id": di, "cdid": cd, "ts": ts, "version": "37.4.2", "region": "IQ"}),
                'Cookie': f"install_id={ii}; device_id={di}; odin_tt={rh(64)}; sessionid={rh(32)}"
            }

            url = f"https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/following/list/?" \
                  f"user_id={ui_}&count=200&page_token={pt}&max_time={mt}&sec_user_id={su}"

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=hd) as resp:
                        rs = await resp.json()

                us = [item['unique_id'] for item in rs.get('followings', [])]
                for u in us:
                    if u not in sn:
                        sn.add(u)
                        au.append(u)

                if not rs.get("has_more"):
                    break

                pt = rs.get("next_page_token", "")
                mt = rs.get("min_time", "")
            except:
                break

        return sorted(au)  # ترتيب Followings
    except Exception as e:
        return {"error": str(e)}

# ----- دالة لجلب Followers -----
async def get_followers(username):
    try:
        m = ms4.InfoTik.TikTok_Info(username)
        ui_ = m["id"]
        up = f'https://www.tiktok.com/@{username}'

        async with aiohttp.ClientSession() as s:
            async with s.get(up, headers={'User-Agent': ua_gen.random if ua_gen else ra()}) as r:
                rt = await r.text()

        su = re.search(r'"secUid":"([^"]+)"', rt).group(1)
        ii = rn(19)
        di = rn(19)
        cd = ru()
        ou = rh(16)
        sn = set()
        au = []
        pt = ""
        mt = ""

        while True:
            ts = int(time.time())
            ua = ra()
            hd = {
                'User-Agent': ua,
                'Accept-Encoding': "gzip",
                'rpc-persist-pyxis-policy-v-tnc': "1",
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
                'X-Tt-Params': gp({"iid": ii, "device_id": di, "cdid": cd, "ts": ts, "version": "37.4.2", "region": "IQ"}),
                'Cookie': f"install_id={ii}; device_id={di}; odin_tt={rh(64)}; sessionid={rh(32)}"
            }

            url = f"https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/follower/list/?" \
                  f"user_id={ui_}&count=200&page_token={pt}&max_time={mt}&sec_user_id={su}"

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=hd) as resp:
                        rs = await resp.json()

                us = [item['unique_id'] for item in rs.get('followers', [])]
                for u in us:
                    if u not in sn:
                        sn.add(u)
                        au.append(u)

                if not rs.get("has_more"):
                    break

                pt = rs.get("next_page_token", "")
                mt = rs.get("min_time", "")
            except:
                break

        return sorted(au)  # ترتيب Followers
    except Exception as e:
        return {"error": str(e)}

# ----- API رئيسية -----
@app.route("/tiktok_users", methods=["GET"])
def api_tiktok_users():
    users = request.args.get("users")
    if not users:
        return jsonify({"status": "error", "message": "send ?users=user1,user2"}), 400

    usernames = [u.strip() for u in users.split(",") if u.strip()]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def fetch_all():
        results = []
        for username in usernames:
            followings = await get_followings(username)
            followers = await get_followers(username)
            results.append({
                "username": username,
                "followings_count": len(followings) if isinstance(followings, list) else 0,
                "followers_count": len(followers) if isinstance(followers, list) else 0,
                "Followings": followings,   # قسم كامل Followings
                "Followers": followers      # قسم كامل Followers
            })
        return results

    results = loop.run_until_complete(fetch_all())
    loop.close()

    return jsonify({
        "status": "success",
        "results": results
    })

# ----- الصفحة الرئيسية -----
@app.route("/")
def home():
    return "🚀 TikTok API Full Followers & Followings Running"

# ----- تشغيل السيرفر -----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
