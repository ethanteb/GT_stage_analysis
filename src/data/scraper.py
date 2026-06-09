import requests, time, re
from bs4 import BeautifulSoup
from .data_structures import Stage_URL

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
    

def no_stages_in_year(url: str) -> int:
    """Returns the number of stages for a given year, based on known historical data. Defaults to 21 stages for modern years."""
    soup = fetch_page(url)
    title_line = soup.find("div", class_="title-line2")
    text = title_line.get_text(" ", strip=False)
    match = re.search(r'(\d+)\s+Stages', text)
    if match:
        num_stages = int(match.group(1))
    else:
        raise ValueError(f"Could not determine number of stages from page: {url}")
    return num_stages


def url_builder(base_url: str, race: str, year: int) -> list[Stage_URL]:
    """Constructs the procyclingstats URL for a given race, year and returns as dict with keys like 
    'giro_2026_15' (Giro 2026, Stage 15) and values as string of the URL."""
    if race.lower() == "giro":
        full_race_name = "giro-d-italia"
    elif race.lower() == "tour":
        full_race_name = "tour-de-france"
    elif race.lower() == "vuelta":
        full_race_name = "vuelta-a-espana"
    else:
        raise ValueError(f"Unsupported race name: {race}")
    stage_urls = []
    no_stages = no_stages_in_year(f"{base_url}/{full_race_name}/{year}")
    for stage in range(1, no_stages + 1):
        try:
            url = f"{base_url}/{full_race_name}/{year}/stage-{stage}"
            stage_url = Stage_URL(race, year, stage, url)
            stage_urls.append(stage_url)
        except ValueError:
            pass
    return stage_urls
    

def url_iterator(base_url: str, start_year: int, end_year: int) -> list[Stage_URL]:
    """Generates URLs for all stages of all 3 GTs for the specified year range, returns as dict with keys like 
    'giro_2026_15' (Giro 2026, Stage 15) and values as strings of the corresponding URL."""
    if start_year > end_year:
        raise ValueError("Start year must be less than or equal to end year.")
    if start_year < 1910 or end_year > 2025:
        raise ValueError("Year range must be between 1910 and 2025.")
    urls = []
    for year in range(start_year, end_year + 1):
        for race in ["giro", "tour", "vuelta"]:
            year_list = url_builder(base_url, race, year)
            urls.extend(year_list)
    return urls
