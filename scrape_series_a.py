import csv
import requests
from bs4 import BeautifulSoup

URL = "https://fundraiseinsider.com/blog/series-a-startups/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

html = requests.get(URL, headers=HEADERS, timeout=60)
html.raise_for_status()
soup = BeautifulSoup(html.text, "lxml")

table = next(
    t for t in soup.find_all("table")
    if "company" in t.get_text(" ", strip=True).lower()[:200]
)

rows = []
for tr in table.find_all("tr"):
    cells = [c.get_text(" ", strip=True).replace("﻿", "") for c in tr.find_all(["th", "td"])]
    if cells:
        rows.append(cells)

header, data = rows[0], rows[1:]

seen, unique = set(), []
for r in data:
    key = (r[0].lower(), r[2].lower() if len(r) > 2 else "")
    if key not in seen:
        seen.add(key)
        unique.append(r)

with open("series_a_startups.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(unique)

print(f"Saved {len(unique)} companies ({len(data) - len(unique)} duplicates removed)")
