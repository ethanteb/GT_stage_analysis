import requests
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; research-bot/1.0)"}

def fetch_page(url: str, delay: float = 1.0) -> BeautifulSoup:
    """Fetches the content of a web page and returns a BeautifulSoup object, with a delay to avoid overwhelming the server."""
    try:
        time.sleep(delay)  # Avoid overwhelming the server
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return BeautifulSoup("<html><body><h1>Error fetching page</h1></body></html>", 'html.parser')
    
def url_builder(base_url: str, race: str, year: int, stage: int) -> str:
    """Constructs the procyclingstats URL for a given race, year, and stage number."""
    if race.lower() == "giro":
        full_race_name = "giro-d-italia"
    elif race.lower() == "tour":
        full_race_name = "tour-de-france"
    elif race.lower() == "vuelta":
        full_race_name = "vuelta-a-espana"
    else:
        raise ValueError(f"Unsupported race name: {race}")
    if not 0 < stage < 22:
        raise ValueError(f"Invalid stage number: {stage}")
    return f"{base_url}/{full_race_name}/{year}/stage-{stage}"