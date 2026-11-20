import os, json, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

CHANNEL_ID = os.environ["CHANNEL_ID"]
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
NS = {"a": "http://www.w3.org/2005/Atom",
      "yt": "http://www.youtube.com/xml/schemas/2015"}

feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
req = urllib.request.Request(feed_url, headers={"User-Agent": "Mozilla/5.0"})
root = ET.fromstring(urllib.request.urlopen(req).read())

limite = datetime.now(timezone.utc) - timedelta(hours=24)

for e in reversed(root.findall("a:entry", NS)):
    pub = datetime.fromisoformat(e.find("a:published", NS).text)
    if pub < limite:
        continue
    vid = e.find("yt:videoId", NS).text
    titre = e.find("a:title", NS).text
    payload = {
        "username": "VOD MAN",
        "avatar_url": "https://i.ibb.co/jPHQZN47/WALLACE-MAN.jpg",
        "content": f"🍿 **Nouvelle VOD disponible !**\n\n**{titre}**\nhttps://www.youtube.com/watch?v={vid}",
    }
    r = urllib.request.Request(
        WEBHOOK, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    )
    urllib.request.urlopen(r)
