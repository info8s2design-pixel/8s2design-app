#!/usr/bin/env python3
"""Convert Wix RSS to local JSON, using only Python stdlib."""
import datetime as dt
import email.utils
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

RSS = "https://8s2design.wixsite.com/home/blog/blog-feed.xml"
DEST = Path(__file__).resolve().parents[1] / "data" / "blog.json"
MEDIA = "{http://search.yahoo.com/mrss/}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"
DC = "{http://purl.org/dc/elements/1.1/}"

def clean_markup(value):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()

def image_from_markup(markup):
    match = re.search(r"<img\b[^>]*?\bsrc=[\"']([^\"']+)", markup or "", re.I)
    return html.unescape(match.group(1)) if match else ""

def valid_image(url):
    parsed = urlparse(url or "")
    return url if parsed.scheme == "https" and parsed.hostname in {"static.wixstatic.com", "images.wixstatic.com", "8s2design.wixsite.com"} else ""

def date_iso(raw):
    try:
        d = email.utils.parsedate_to_datetime(raw)
        return d.astimezone(dt.timezone.utc).isoformat()
    except (ValueError, TypeError, IndexError, OverflowError, AttributeError):
        try: return dt.datetime.fromisoformat(raw.replace("Z", "+00:00")).isoformat()
        except (ValueError, AttributeError): return ""

def extract(root):
    posts = []
    for item in root.findall(".//item"):
        title = clean_markup(item.findtext("title"))
        link = (item.findtext("link") or "").strip()
        parsed = urlparse(link)
        if not title or parsed.scheme != "https" or parsed.hostname not in {"8s2design.wixsite.com", "www.8s2design.wixsite.com"}: continue
        desc = item.findtext("description") or ""
        body = item.findtext(CONTENT + "encoded") or ""
        summary = clean_markup(desc or body)[:230]
        image = ""
        for node in item.findall(MEDIA + "content") + item.findall(MEDIA + "thumbnail") + item.findall("enclosure"):
            candidate = node.attrib.get("url", "")
            if valid_image(candidate): image = candidate; break
        if not image: image = valid_image(image_from_markup(desc) or image_from_markup(body))
        posts.append({"title": title[:200], "url": link, "date": date_iso(item.findtext("pubDate") or item.findtext(DC + "date") or ""), "summary": summary, "image": image})
    return posts[:30]

def main():
    req = Request(RSS, headers={"User-Agent": "8S2DesignBlogSync/1.0", "Accept": "application/rss+xml, application/xml, text/xml"})
    with urlopen(req, timeout=30) as response:
        xml = response.read(5_000_000)
    posts = extract(ET.fromstring(xml))
    if not posts: raise RuntimeError("Nessun articolo RSS valido: JSON esistente mantenuto.")
    result = {"source": RSS, "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(), "posts": posts}
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Sincronizzati {len(posts)} articoli")

if __name__ == "__main__": main()
