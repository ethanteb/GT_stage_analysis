import requests, time, re
from bs4 import BeautifulSoup

'''3 classes defining the data structures that are used to store the page urls, the stage profile and the individual ride stage results.'''
class RiderStageResult:
    """Represents one rider's result for one stage of a Grand Tour."""
    def __init__(
        self,
        race: str,
        year: int,
        stage_number: int,
        rider_name: str,
        team: str,
        time: str,
        gap: str | None,
        rank: int, 
        breakaway: bool = False,
        breakaway_distance: int = 0
    ):
        self.race               = race
        self.year               = year
        self.stage_number       = stage_number
        self.rider_name         = rider_name
        self.team               = team
        self.time               = time
        self.gap                = gap
        self.rank               = rank
        self.breakaway          = breakaway
        self.breakaway_distance = breakaway_distance

    def __str__(self) -> str:
        """Useful for printing results in a readable format."""
        gap_str = self.gap if self.gap else "winner"
        return_string = f"[{self.race.upper()} {self.year} | Stage {self.stage_number}] "
        return_string += f"P{self.rank} - {self.rider_name} ({self.team}) "
        return_string += f"| {self.time} | Gap: {gap_str}"
        if self.breakaway:
            return_string += f" | Breakaway: {self.breakaway_distance}km"
        return (return_string)

    def to_dict(self) -> dict:
        """Convert to a dictionary, useful for CSV/JSON export."""
        return {
            "race":         self.race,
            "year":         self.year,
            "stage_number": self.stage_number,
            "rider_name":   self.rider_name,
            "team":         self.team,
            "time":         self.time,
            "gap":          self.gap,
            "rank":         self.rank,
            "breakaway":     self.breakaway,
            "breakaway_distance": self.breakaway_distance
        }
    
    
class StageProfile:
    """Represents the profile of a stage, including type and distance."""
    def __init__(
        self,
        race: str,
        year: int,
        stage_number: int, 
        date: str, 
        start_time: str, 
        avg_speed_winner_kmh: float, 
        classification: str, 
        race_category: str, 
        distance_km: float, 
        gradient_final_km: float, 
        profile_score: int, 
        vertical_metres: int,
        departure_location: str,
        arrival_location: str,
        race_ranking: int,
        won_how: str,
        avg_temperature_c: float
    ):
        self.race = race
        self.year = year
        self.stage_number = stage_number
        self.date = date
        self.start_time = start_time
        self.avg_speed_winner_kmh = avg_speed_winner_kmh
        self.classification = classification
        self.race_category = race_category
        self.distance_km = distance_km
        self.gradient_final_km = gradient_final_km
        self.profile_score = profile_score
        self.vertical_metres = vertical_metres
        self.departure_location = departure_location
        self.arrival_location = arrival_location
        self.race_ranking = race_ranking
        self.won_how = won_how
        self.avg_temperature_c = avg_temperature_c

    def __str__(self) -> str:
        """Useful for printing stage profile in a readable format."""
        return (
            f"{self.race.upper()} {self.year} | Stage {self.stage_number} | "
            f"Date: {self.date} | Start Time: {self.start_time} | Classification: {self.classification} | Race category: {self.race_category}\n"
            f"Distance: {self.distance_km}km | Avg. speed winner: {self.avg_speed_winner_kmh}km/h | Gradient final km: {self.gradient_final_km}% | "
            f"Profile score: {self.profile_score} | Vertical climb: {self.vertical_metres}m\nDeparture: {self.departure_location} | Arrival: {self.arrival_location} | "
            f"PCS Race Ranking: {self.race_ranking} | Won how: {self.won_how} | Avg. temperature: {self.avg_temperature_c}°C"
        )
    
    def to_dict(self) -> dict:
        """Convert to a dictionary, useful for CSV/JSON export."""
        return {
            "race":                 self.race,
            "year":                 self.year,
            "stage_number":         self.stage_number,
            "date":                 self.date,
            "start_time":           self.start_time,
            "avg_speed_winner_kmh": self.avg_speed_winner_kmh,
            "classification":       self.classification,
            "race_category":        self.race_category,
            "distance_km":          self.distance_km,
            "gradient_final_km":    self.gradient_final_km,
            "profile_score":        self.profile_score,
            "vertical_metres":      self.vertical_metres,
            "departure_location":   self.departure_location,
            "arrival_location":     self.arrival_location,
            "race_ranking":         self.race_ranking,
            "won_how":              self.won_how,
            "avg_temperature_c":    self.avg_temperature_c
        }
    
class StageURL:
    """Represents the URL for a specific stage of a Grand Tour."""
    def __init__(self, race: str, year: int, stage_number: int, url: str):
        self.race           = race.upper()
        self.year           = year
        self.stage_number   = stage_number
        self.url            = url

    def __str__(self) -> str:
        """Useful for printing stage URL in a readable format."""
        return f"{self.race} {self.year} | Stage {self.stage_number} | URL: {self.url}"


'''Functions that are used for scraping and parsing the data from procycling stats'''
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


def url_builder(base_url: str, race: str, year: int) -> list[StageURL]:
    """Constructs the procyclingstats URL for a given race, year and returns as list of
    StageURL dataclass instances for each stage."""
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
            stage_url = StageURL(race, year, stage, url)
            stage_urls.append(stage_url)
        except ValueError:
            pass
    return stage_urls
    

def url_iterator(base_url: str, start_year: int, end_year: int) -> list[StageURL]:
    """Generates URLs for all stages of all 3 GTs for the specified year range, returns as list of StageURL instances."""
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

def parse_stage_results(stage_url: StageURL, soup: BeautifulSoup) -> list[RiderStageResult]:
    """First obtains then parses a BeautifulSoup object of a stage results page and extracts structured data for each rider's result, also returning the beautiful soup object."""

    race = stage_url.race
    year = stage_url.year
    stage_number = stage_url.stage_number

    results = [] # List to hold parsed results
    table = soup.select_one("div#resultsCont table.results tbody") # Locates the results table

    for row in table.select("tr"):
        cells = row.select("td")
        if not cells:
            continue

        rank_text = cells[0].get_text(strip=True)
        if not rank_text.isdigit():
            continue
        rank = int(rank_text)

        # Rider name: first <a> inside .ridername, combining both spans/text nodes
        ridername_td = row.select_one("td.ridername")
        rider_link = ridername_td.select_one("a") if ridername_td else None
        if rider_link:
            # Concatenate all text parts: spans + tail text (e.g. "Dversnes Lavik" + "Fredrik")
            parts = [s.get_text(strip=True) for s in rider_link.find_all("span", class_="uppercase")]
            tail = rider_link.find("span", class_="uppercase").next_sibling
            if tail:
                tail_text = tail.strip() if isinstance(tail, str) else tail.get_text(strip=True)
                if tail_text:
                    parts.append(tail_text)
            rider = " ".join(parts)
        else:
            rider = ""

        shield = ridername_td.select_one("div.svg_shield") if ridername_td else None

        if shield and shield.get("title"):
            breakaway = True
            breakaway_description = shield["title"]  # e.g. "153 kilometre in a group in front of the peloton"
            # Extract just the distance in km
            match = re.search(r"(\d+)\s*kilometre", breakaway_description)
            breakaway_distance = int(match.group(1)) if match else None
        else:
            breakaway = False
            breakaway_distance = None

        # Team name: <a> inside td.cu600 (skip mobile duplicate inside ridername)
        team_td = row.select_one("td.cu600")
        team = team_td.select_one("a").get_text(strip=True) if team_td and team_td.select_one("a") else ""

        # Time: prefer the <span class="hide"> which has clean text, fall back to <font>
        time_td = row.select_one("td.time")
        if time_td:
            hidden = time_td.select_one("span.hide")
            time = hidden.get_text(strip=True) if hidden else time_td.select_one("font").get_text(strip=True)
        else:
            time = ""

        # Gap: GC timelag column (index 2), e.g. "+2:41:57"; strip for rank 1 (will be empty or "0")
        gap_text = cells[2].get_text(strip=True) if len(cells) > 2 else ""
        gap = gap_text if gap_text and gap_text != "0" else None

        rider_stage_result = RiderStageResult(race, year, stage_number, rider, team, time, gap, rank, breakaway, breakaway_distance)
        results.append(rider_stage_result)
    return results


def parse_stage_profile(stage_url: StageURL, soup: BeautifulSoup) -> StageProfile:
    """Parses the stage profile information (type and distance) from the BeautifulSoup object and the StageURL object."""
    data = {} # Dictionary to hold parsed profile data before converting to StageProfile dataclass

    for li in soup.find_all("li"):
        title = li.find("div", class_="title")
        value = li.find("div", class_="value")
        if title and value:
            key = title.get_text(strip=True).rstrip(":")
            val = value.get_text(" ", strip=True)
            data[key] = val
    
    match = re.search(r'(-?\d+)\s*km', data.get("Distance"))
    if match:
        distance_km = int(match.group(1))

    match = re.search(r'(-?\d+(?:\.\d+)?)\s*km/h', data.get("Avg. speed winner"))
    if match:
        winner_speed_kmh = float(match.group(1))

    match = re.search(r'(-?\d+(?:\.\d+)?)\s*%', data.get("Gradient final km"))
    if match:
        grad_final_km = float(match.group(1))

    match = re.search(r'(-?\d+)\s*°C', data.get("Avg. temperature"))
    if match:
        temperature_c = int(match.group(1))

    stage_profile = StageProfile(
        stage_url.race,
        stage_url.year, 
        stage_url.stage_number,
        data.get("Date"), 
        data.get("Start time"), 
        winner_speed_kmh, 
        data.get("Classification"), 
        data.get("Race category"), 
        distance_km,
        grad_final_km, 
        data.get("ProfileScore"), 
        data.get("Vertical meters"), 
        data.get("Departure"), 
        data.get("Arrival"), 
        data.get("Race ranking"),
        data.get("Won how"), 
        temperature_c
    )
    return stage_profile
