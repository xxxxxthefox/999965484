import aiohttp
import asyncio
import time
import random
import string
import uuid
import hashlib
import base64
import json
import re
import cloudscraper
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ================== أدوات مساعدة ==================
def rn(l=10):
    return ''.join(random.choice(string.digits) for _ in range(l))

def rh(l=32):
    return ''.join(random.choice('0123456789abcdef') for _ in range(l))

def ru():
    return str(uuid.uuid4())

def gx(ts):
    return "8404" + hashlib.md5(str(ts).encode()).hexdigest()[:30]

def ga(ts, di, ii):
    raw = f"{di}:{ii}:{ts}"
    return base64.b64encode(hashlib.sha256(raw.encode()).digest()).decode()

def gp(data):
    return base64.b64encode(json.dumps(data, separators=(',', ':')).encode()).decode()

def user_agent():
    brands = ["Samsung","Xiaomi","Huawei","Realme","Infinix","Oppo","Vivo","Tecno"]
    models = ["A52","Note9","P30","X692","M21","Y20","C25","F17"]
    android = random.choice(["10","11","12","13"])
    return f"com.zhiliaoapp.musically.go/370402 (Linux; Android {android}; {random.choice(brands)} {random.choice(models)}; Build/{rh(6)})"

# ================== جلب معلومات حساب TikTok ==================
def tiktok_info(username):
    try:
        scraper = cloudscraper.create_scraper()
        r = scraper.get(
            f"https://www.tiktok.com/@{username}",
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        tag = soup.find("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")
        if not tag:
            return None

        data = json.loads(tag.text)
        info = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
        user = info["user"]
        stats = info["stats"]

        return {
            "username": username,
            "nickname": user.get("nickname"),
            "bio": user.get("signature"),
            "followers": stats.get("followerCount"),
            "following": stats.get("followingCount"),
            "likes": stats.get("heartCount"),
            "videos": stats.get("videoCount"),
            "region": user.get("region"),
            "verified": user.get("verified"),
            "url": f"https://www.tiktok.com/@{username}"
        }
    except:
        return None

# ================== سحب المتابَعين ==================
async def pull_followings(username):
    ii = rn(19)
    di = rn(19)
    ts = int(time.time())

    headers = {
        "User-Agent": user_agent(),
        "x-gorgon": gx(ts),
        "x-khronos": str(ts),
        "x-argus": ga(ts, di, ii),
        "X-Tt-Params": gp({
            "iid": ii,
            "device_id": di,
            "ts": ts,
            "version": "37.4.2",
            "region": "IQ"
        })
    }

    # URL أساسي لسحب المتابَعين (Lite API)
    url = (
        f"https://api16-normal-c-alisg.tiktokv.com/lite/v2/relation/following/list/"
        f"?user_id={username}&count=50"
    )

    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, headers=headers) as r:
                data = await r.json()
                return [u["unique_id"] for u in data.get("followings", [])]
    except:
        return []

# ================== API ==================
@app.route("/scan", methods=["GET"])
def scan():
    username = request.args.get("username", "").replace("@","").strip()
    if not username:
        return jsonify({"status":"error","message":"username required"}), 400

    # جلب followings
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    followings = loop.run_until_complete(pull_followings(username))
    loop.close()

    results = []
    for u in followings:
        info = tiktok_info(u)
        if info:
            results.append(info)

    return jsonify({
        "status": "success",
        "source_user": username,
        "total_accounts": len(results),
        "accounts": results
    })

@app.route("/")
def home():
    return "✅ TikTok Scan API is Running"

# ================== تشغيل ==================
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))