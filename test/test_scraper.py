import asyncio
import json
import os
from smarttooler_sraper.scraper import scrape_from_seeds

def test_scraper_run():
    # Remove previous output if exists
    if os.path.exists("data/tools.json"):
        os.remove("data/tools.json")

    asyncio.run(scrape_from_seeds())

    assert os.path.exists("data/tools.json"), "Output file not created."

    with open("data/tools.json") as f:
        links = json.load(f)

    assert isinstance(links, list), "Output is not a list."
    assert len(links) > 0, "No links were scraped."
    assert any("github.com" in link for link in links), "Expected GitHub links not found."

    print("✅ Test passed: scraper collected", len(links), "links.")

if __name__ == "__main__":
    test_scraper_run()
