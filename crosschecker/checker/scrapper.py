import requests
from bs4 import BeautifulSoup


def scrape_wikipedia(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    text = " ".join([p.get_text(strip=False) for p in paragraphs])
    return text
