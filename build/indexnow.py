#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Seznam, Naver) with every URL in sitemap.xml, or the URLs given as arguments.
Usage: python3 build/indexnow.py [url ...]"""
import json, re, sys, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from data import SITE
key = SITE["indexnow_key"]
urls = sys.argv[1:] or re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text())
body = json.dumps({"host": SITE["url"].split("//")[1], "key": key, "keyLocation": f"{SITE['url']}/{key}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow:", r.status, f"({len(urls)} URLs)")
except Exception as e:
    print("IndexNow ping failed (site must be live first):", e)
