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
import telebot
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from flask_cors import CORS

BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)
ss = {}
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

async def pu(dk):
    try:
        m = ms4.InfoTik.TikTok_Info(dk)
        ui_ = m["id"]
        up = f'https://www.tiktok.com/@{dk}'
        async with aiohttp.ClientSession() as s:
            async with s.get(up, headers={'User-Agent': ua_gen.random}) as r:
                rt = await r.text()
        su = re.search(r'"secUid":"([^"]+)"', rt).group(1)
        ii = rn(19)
        di = rn(19)
        cd = ru()
        ou = rh(16)
        sn = set()
        followers_info = []
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
                  f"sss-network-channel={rn(13)}&user_id={ui_}&count=200&page_token={pt}&max_time={mt}&source_type=4" \
                  f"&request_tag_from=h5&sec_user_id={su}" \
                  f"&manifest_version_code=370402&_rticket={rn(13)}&app_language=ar&app_type=normal" \
                  f"&iid={ii}&app_package=com.zhiliaoapp.musically.go&channel=googleplay&device_type=Infinix+X692" \
                  f"&language=ar&host_abi=arm64-v8a&locale=ar&resolution=720*1464&openudid={ou}&update_version_code=370402" \
                  f"&ac2=wifi&cdid={cd}&sys_region=EG&os_api=29&timezone_name=Asia%2FBaghdad&dpi=320" \
                  f"&carrier_region=IQ&ac=wifi&device_id={di}&os_version=10&timezone_offset=10800&version_code=370402" \
                  f"&app_name=musically_go&ab_version=37.4.2&version_name=37.4.2&device_brand=Infinix&op_region=IQ&ssmix=a" \
                  f"&device_platform=android&build_number=37.4.2&region=EG&aid=1340&ts={ts}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=hd) as resp:
                        rs = await resp.json()
                us = [item['unique_id'] for item in rs.get('followings', [])]
                for u in us:
                    if u not in sn:
                        sn.add(u)
                        info = ms4.InfoTik.TikTok_Info(u)
                        followers_info.append({
                            "User": f"@{u}",
                            "Name": info.get('nickname', 'لا يوجد'),
                            "Followers": info.get('followers', 0),
                            "Following": info.get('following', 0),
                            "Likes": info.get('likes', 0),
                            "Videos": info.get('videos', 0),
                            "Verified": "موثق" if info.get('verified') else "ماموثق",
                            "Country": info.get('region', 'IQ'),
                            "Bio": info.get('bio', 'لا يوجد'),
                            "Url": f"https://www.tiktok.com/@{u}"
                        })
                if not rs.get("has_more"):
                    break
                pt = rs.get("next_page_token", "")
                mt = rs.get("min_time", "")
            except:
                break
        return followers_info
    except:
        return []

# ---------- Flask API ----------
app = Flask(__name__)
CORS(app)

@app.route('/followers', methods=['POST'])
def followers():
    data = request.json
    usernames = data.get('usernames', [])
    if not usernames:
        return jsonify({"error": "يرجى ارسال قائمة يوزرات"}), 400
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = {}
    for username in usernames:
        result[username] = loop.run_until_complete(pu(username))
    loop.close()
    return jsonify(result)

# ---------- تشغيل السيرفر ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
