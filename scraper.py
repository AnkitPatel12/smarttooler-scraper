import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os

SEED_URLS = [
    "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md",
]

visited = set()
found_links = set()

async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def extract_links_from_markdown(markdown_text):
    pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    return re.findall(pattern, markdown_text)

async def scrape_from_url(session, url, depth=0, max_depth=1):
    if url in visited or depth > max_depth:
        return

    visited.add(url)
    print(f"Scraping {url} (depth {depth})")
    text = await fetch(session, url)

    links = extract_links_from_markdown(text)
    for title, link in links:
        found_links.add(link)
        if "github.com" in link and "/awesome" in link:
            await scrape_from_url(session, link, depth + 1, max_depth)

async def scrape_from_seeds():
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_from_url(session, seed) for seed in SEED_URLS]
        await asyncio.gather(*tasks)

    print(f"\nTotal unique links found: {len(found_links)}")
    os.makedirs("data", exist_ok=True)
    with open("data/tools.json", "w") as f:
        import json
        json.dump(sorted(found_links), f, indent=2)
