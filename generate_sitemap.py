# generate_sitemap.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import datetime

BASE_URL = "https://www.siai.co.zw"
CRAWLED = set()
TO_CRAWL = [BASE_URL]

def get_links(url):
    try:
        resp = requests.get(url, timeout=10)
        if not resp.headers["Content-Type"].startswith("text/html"):
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        links = set()
        for tag in soup.find_all("a", href=True):
            href = urljoin(url, tag["href"])
            parsed_href = urlparse(href)
            if BASE_URL in href and parsed_href.path.endswith((".html", "/")):
                links.add(href.split("#")[0])
        return list(links)
    except Exception as e:
        print(f"⚠️ Error fetching {url}: {e}")
        return []

while TO_CRAWL:
    url = TO_CRAWL.pop()
    if url in CRAWLED:
        continue
    CRAWLED.add(url)
    TO_CRAWL.extend([link for link in get_links(url) if link not in CRAWLED])

today = datetime.datetime.now().date()
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url in sorted(CRAWLED):
    sitemap += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"

sitemap += "</urlset>"

# Save inside your Flask static folder
with open("static/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)

print("✅ Sitemap generated at static/sitemap.xml")
