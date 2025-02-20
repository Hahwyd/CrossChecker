import requests
from bs4 import BeautifulSoup
from typing import Optional


def scrape_wikipedia(url: str) -> Optional[str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")

    # if not paragraphs: # Need to add to logging
    #     print(f"No paragraphs found at {url}")
    #     return None

    text = " ".join([p.get_text(strip=False) for p in paragraphs])
    return text

print(scrape_wikipedia("https://en.wikipedia.org/wiki/Tomato"))