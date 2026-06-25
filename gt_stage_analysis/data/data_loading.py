#-------------------------------------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------------------------------------

import requests, time, re, json
import pandas as pd
from bs4 import BeautifulSoup
from dataclasses import dataclass, fields

#-------------------------------------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------------------------------------

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; research-bot/1.0)"}
GRAND_TOURS: dict[str, str] = {'giro': 'giro-d-italia', 'tour': 'tour-de-france', 'vuelta': 'vuelta-a-espana'}
BASE_URL = "https://www.procyclingstats.com/race"

#-------------------------------------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------------------------------------

def fetch_page(url: str, delay: float = 1.0) -> BeautifulSoup:
    """Fetches page content from url and returns a BeautifulSoup object.
    Includes delay (in seconds) to be polite to the server."""
    time.sleep(delay)
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        print(f'Fetched: {url}')
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as exc:
        print(f"Error fetching {url}: {exc}")
        return BeautifulSoup(
            "<html><body><h1>Error fetching page</h1></body></html>",
            "html.parser",
        )
    
def _parse_float(text: str, pattern: str) -> float:
    """Return the first captured float from text matching pattern, or None."""
    if text is None:
        return None
    m = re.search(pattern, text)
    return float(m.group(1)) if m else None
 
 
def _parse_int(text: str, pattern: str) -> int:
    """Return the first captured int from text matching pattern, or None."""
    if text is None:
        return None
    m = re.search(pattern, text)
    return int(m.group(1)) if m else None

#-------------------------------------------------------------------------------------------------------------
# Data Classes
#-------------------------------------------------------------------------------------------------------------

@dataclass
class StageProfile:
    """Stage metadata scraped from the profile section of a PCS stage page."""
    race: str
    year: int
    stage_number: int
    date: str
    start_time: str
    avg_speed_winner_kmh: float
    classification: str
    race_category: str
    distance_km: float
    gradient_final_km: float
    profile_score: int
    vertical_metres: int
    departure_location: str
    arrival_location: str
    race_ranking: int
    won_how: str
    avg_temperature_c: float

    def __str__(self) -> str:
        return (
            f"{self.race.upper()} {self.year} | Stage {self.stage_number} | "
            f"Date: {self.date} | Start Time: {self.start_time} | Classification: {self.classification} | Race category: {self.race_category}\n"
            f"Distance: {self.distance_km}km | Avg. speed winner: {self.avg_speed_winner_kmh}km/h | Gradient final km: {self.gradient_final_km}% | "
            f"Profile score: {self.profile_score} | Vertical climb: {self.vertical_metres}m\nDeparture: {self.departure_location} | Arrival: {self.arrival_location} | "
            f"PCS Race Ranking: {self.race_ranking} | Won how: {self.won_how} | Avg. temperature: {self.avg_temperature_c}°C"
        )
    
    def to_dict(self) -> dict:
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
    
    @classmethod
    def from_dict(cls, data: dict) -> StageProfile:
        return cls(
            race=data["race"],
            year=data["year"],
            stage_number=data["stage_number"],
            date=data["date"],
            start_time=data["start_time"],
            avg_speed_winner_kmh=data["avg_speed_winner_kmh"],
            classification=data["classification"],
            race_category=data["race_category"],
            distance_km=data["distance_km"],
            gradient_final_km=data["gradient_final_km"],
            profile_score=data["profile_score"],
            vertical_metres=data["vertical_metres"],
            departure_location=data["departure_location"],
            arrival_location=data["arrival_location"],
            race_ranking=data["race_ranking"],
            won_how=data["won_how"],
            avg_temperature_c=data["avg_temperature_c"]
        )

@dataclass
class RiderStageResult:
    """Data structure class containing an individual rider's result in a single stage of a specific grand tour"""
    race: str
    year: int
    stage_number: int
    rider_name: str
    team: str
    time: str
    gap: str | None
    rank: int 
    breakaway_distance: int | None

    def __str__(self) -> str:
        gap_str = self.gap if self.gap else "winner"
        s = f"[{self.race.upper()} {self.year} | Stage {self.stage_number}] "
        s += f"P{self.rank} - {self.rider_name} ({self.team}) "
        s += f"| {self.time} | Gap: {gap_str}"
        if self.breakaway_distance:
            s += f" | Breakaway: {self.breakaway_distance}km"
        return s

    def to_dict(self) -> dict:
        return {
            "race":         self.race,
            "year":         self.year,
            "stage_number": self.stage_number,
            "rider_name":   self.rider_name,
            "team":         self.team,
            "time":         self.time,
            "gap":          self.gap,
            "rank":         self.rank,
            "breakaway_distance": self.breakaway_distance
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> RiderStageResult:
        return cls(
            race=data["race"],
            year=data["year"],
            stage_number=data["stage_number"],
            rider_name=data["rider_name"],
            team=data["team"],
            time=data["time"],
            gap=data["gap"],
            rank=data["rank"],
            breakaway_distance=data["breakaway_distance"]
        )

#-------------------------------------------------------------------------------------------------------------
# GTStage: Corresponds to a single stage, parses own data
#-------------------------------------------------------------------------------------------------------------


class GTStage:
    """Represents a single stage of a Grand Tour.
    Call fetch_page first, then parse_stage_profile and then parse_stage_results` as needed."""
    def __init__(self, race: str, year: int, stage_number: int, url: str):
        self.race           = race.upper()
        self.year           = year
        self.stage_number   = stage_number
        self.url            = url
        self.page_content   : BeautifulSoup | None = None
        self.stage_profile  : StageProfile | None = None
        self.stage_results  : list[RiderStageResult]

    def __str__(self) -> str:
        s = f"{self.race} {self.year} | Stage {self.stage_number} | URL: {self.url}"
        s += " | Content: TRUE" if self.page_content else ""
        s += " | Profile: TRUE" if self.stage_profile else ""
        s += " | Results: TRUE" if self.stage_results else ""
        return s
    
    def to_dict(self):
        return {
            "race": self.race,
            "year": self.year,
            "stage_number": self.stage_number,
            "url": self.url,
            # Not saving BeautifulSoup objects
            "stage_profile": (self.stage_profile.to_dict() if self.stage_profile is not None else None),
            "stage_results": [result.to_dict()for result in self.stage_results]
        }
    
    @classmethod
    def from_dict(cls, data):
        obj = cls(
            race=data["race"],
            year=data["year"],
            stage_number=data["stage_number"],
            url=data["url"]
        )
        if data["stage_profile"] is not None:
            obj.stage_profile = StageProfile.from_dict(data["stage_profile"])
        obj.stage_results = [RiderStageResult.from_dict(result_data) for result_data in data["stage_results"]]
        return obj
    
    #--------------------------------------------------------------------------------------------------------
    # Fetching
    #--------------------------------------------------------------------------------------------------------
    
    def fetch_page(self, delay: float = 1.0):
        """Download the stage page and store it as page_content."""
        self.page_content = fetch_page(self.url, delay=delay)
 
    def _require_page(self) -> BeautifulSoup:
        """Return page_content, raising an error if it hasn't been fetched."""
        if self.page_content is None:
            raise RuntimeError(f"Page not fetched yet for {self}. Call fetch_page() first.")
        return self.page_content
    
    #--------------------------------------------------------------------------------------------------------
    # Parsing Stage Profile
    #--------------------------------------------------------------------------------------------------------
    
    def parse_stage_profile(self) -> None:
        """Parse the profile metadata and populate stage_profile."""
        soup = self._require_page() # check page content has been retrieved
 
        # Collect every title/value pair from <li> elements
        data: dict[str, str] = {}
        for li in soup.find_all("li"):
            title = li.find("div", class_="title")
            value = li.find("div", class_="value")
            if title and value:
                key = title.get_text(strip=True).rstrip(":")
                data[key] = value.get_text(" ", strip=True)
 
        self.stage_profile = StageProfile(
            race                 = self.race,
            year                 = self.year,
            stage_number         = self.stage_number,
            date                 = data.get("Date"),
            start_time           = data.get("Start time"),
            avg_speed_winner_kmh = _parse_float(data.get("Avg. speed winner"), r"(-?\d+(?:\.\d+)?)\s*km/h"),
            classification       = data.get("Classification"),
            race_category        = data.get("Race category"),
            distance_km          = _parse_float(data.get("Distance"), r"(-?\d+(?:\.\d+)?)\s*km"),
            gradient_final_km    = _parse_float(data.get("Gradient final km"), r"(-?\d+(?:\.\d+)?)\s*%"),
            profile_score        = data.get("ProfileScore"),
            vertical_metres      = data.get("Vertical meters"),
            departure_location   = data.get("Departure"),
            arrival_location     = data.get("Arrival"),
            race_ranking         = data.get("Race ranking"),
            won_how              = data.get("Won how"),
            avg_temperature_c    = _parse_int(data.get("Avg. temperature"), r"(-?\d+)\s*°C"),
        )

    #--------------------------------------------------------------------------------------------------------
    # Parsing Stage Results
    #--------------------------------------------------------------------------------------------------------
    
    def parse_stage_results(self) -> None:
        """Parse the results table and populate stage_results."""
        soup  = self._require_page() # check page content has been retrieved
        table = soup.select_one("div#resultsCont table.results tbody")
        if table is None:
            print(f"Results table not found for {self}")
            return
 
        self.stage_results = []
        for row in table.select("tr"):
            result = self._parse_result_row(row)
            if result is not None:
                self.stage_results.append(result)

    def _parse_result_row(self, row) -> RiderStageResult:
        """Parse a single <tr> into a RiderStageResult object."""
        cells = row.select("td")
        if not cells:
            return None
 
        rank_text = cells[0].get_text(strip=True)
        if not rank_text.isdigit():
            return None
        rank = int(rank_text)
 
        # Rider name
        ridername_td = row.select_one("td.ridername")
        rider = self._parse_rider_name(ridername_td)
 
        # Breakaway shield
        breakaway_distance = self._parse_breakaway(ridername_td)
 
        # Team
        team_td = row.select_one("td.cu600")
        team = (
            team_td.select_one("a").get_text(strip=True)
            if team_td and team_td.select_one("a")
            else ""
        )
 
        # Finish time
        time_td = row.select_one("td.time")
        finish_time = ""
        if time_td:
            hidden = time_td.select_one("span.hide")
            font   = time_td.select_one("font")
            finish_time = (
                hidden.get_text(strip=True) if hidden
                else font.get_text(strip=True) if font
                else ""
            )
 
        # Gap to winner (column index 2)
        gap_text = cells[2].get_text(strip=True) if len(cells) > 2 else ""
        gap = gap_text if gap_text and gap_text != "0" else None
 
        return RiderStageResult(
            race               = self.race,
            year               = self.year,
            stage_number       = self.stage_number,
            rider_name         = rider,
            team               = team,
            time               = finish_time,
            gap                = gap,
            rank               = rank,
            breakaway_distance = breakaway_distance,
        )

    @staticmethod
    def _parse_rider_name(ridername_td) -> str:
        if ridername_td is None:
            return ""
        rider_link = ridername_td.select_one("a")
        if rider_link is None:
            return ""
        parts = [s.get_text(strip=True) for s in rider_link.find_all("span", class_="uppercase")]
        first_uppercase = rider_link.find("span", class_="uppercase")
        if first_uppercase:
            tail = first_uppercase.next_sibling
            if tail:
                tail_text = tail.strip() if isinstance(tail, str) else tail.get_text(strip=True)
                if tail_text:
                    parts.append(tail_text)
        return " ".join(parts)
 
    @staticmethod
    def _parse_breakaway(ridername_td) -> int:
        if ridername_td is None:
            return None
        shield = ridername_td.select_one("div.svg_shield")
        if shield and shield.get("title"):
            desc = shield["title"]
            m = re.search(r"(\d+)\s*kilometre", desc)
            return int(m.group(1)) if m else None
        return None
 
#-------------------------------------------------------------------------------------------------------------
# GTResults: controls fetching across years and the three grand tours
#-------------------------------------------------------------------------------------------------------------

class GTResults:
    """Builds and stores GTStage objects for a range of years.
    Usage:
        results = GTResults(BASE_URL, 2022, 2023)
        results.build_stage_list()
        for stage in results.stages:
            stage.fetch_page()
            stage.parse_stage_profile()
            stage.parse_stage_results()
        results.to_json('data/raw/2022_2023_raw')
    """
    def __init__(self, base_url: str, start_year: int, end_year: int):
        self.base_url                         = base_url
        self.start_year                       = start_year
        self.end_year                         = end_year
        self.list_GT_stages  : list[GTStage]  = []
        self.num_stages_dict : dict[str, int] = {} # keys of type 'race_short year' e.g. 'GIRO 2026'

    def to_dict(self):
        return {
            "base_url": self.base_url,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "list_GT_stages": [stage.to_dict() for stage in self.list_GT_stages],
            "num_stages_dict": self.num_stages_dict,
        }
    
    @classmethod
    def from_dict(cls, data):
        obj = cls(
            base_url=data["base_url"],
            start_year=data["start_year"],
            end_year=data["end_year"]
        )
        obj.num_stages_dict = data["num_stages_dict"]
        obj.list_GT_stages = [
            GTStage.from_dict(stage_data)
            for stage_data in data["list_GT_stages"]
        ]
        return obj

    def __str__(self):
        return (f"GTResults(years={self.start_year}-{self.end_year}, stages_loaded={len(self.list_GT_stages)})")
    
    def to_json(self, loc):
        with open(f"{loc}.json", "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load_json(cls, loc):
        with open(f"{loc}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    #--------------------------------------------------------------------------------------------------------
    # Stage count methods
    #--------------------------------------------------------------------------------------------------------

    @staticmethod
    def _count_stages(soup: BeautifulSoup, label: str) -> int:
        """Extract the stage count from a race overview page."""
        title_line = soup.find("div", class_="title-line2")
        if title_line:
            m = re.search(r"(\d+)\s+Stages", title_line.get_text(" ", strip=False))
            if m:
                return int(m.group(1))
        raise ValueError(f"Could not determine stage count for {label}")
 
    def _fetch_stage_count(self, race_short: str, full_name: str, year: int) -> int:
        """Fetch the race overview page and return the number of stages."""
        url  = f"{self.base_url}/{full_name}/{year}"
        soup = fetch_page(url)
        return self._count_stages(soup, f"{race_short.upper()} {year}")
    
    #--------------------------------------------------------------------------------------------------------
    # Breakaway success rate dataframe preparation
    #--------------------------------------------------------------------------------------------------------
    
    def convert_to_breakaway_dataframe(self) -> pd.DataFrame:
        """Defines & populates dataframe including the first column intended to be a bool success or failure"""
        columns = ['break_success']
        df = pd.DataFrame(columns=columns.extend([f.name for f in fields(StageProfile)]))
        rows = []
        for GT_stage in self.list_GT_stages:
            dict = {'break_success': False}
            try:
                if GT_stage.stage_results[0].breakaway_distance:
                    dict = {'break_success': True} 
            except IndexError: #handle situations where the stage has no result list, e.g Vuelta 2025 Stage 11
                pass
            dict.update(GT_stage.stage_profile.to_dict())
            rows.append(dict)
            # print(f"Appended {GT_stage.race}{GT_stage.stage_number}")
        df = pd.DataFrame(rows)
        return df

    #--------------------------------------------------------------------------------------------------------
    # Overall control methods
    #--------------------------------------------------------------------------------------------------------

    def build_stage_list(self):
        """Populate stages by fetching stage counts for each race/year."""
        for year in range(self.start_year, self.end_year + 1):
            for short_name, full_name in GRAND_TOURS.items():
                key = f"{short_name}{year}"
                num_stages = self._fetch_stage_count(short_name, full_name, year)
                self.num_stages_dict[key] = num_stages
                for stage_num in range(1, num_stages + 1):
                    url = f"{self.base_url}/{full_name}/{year}/stage-{stage_num}"
                    self.list_GT_stages.append(GTStage(short_name, year, stage_num, url))