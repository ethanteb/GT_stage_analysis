import re
from bs4 import BeautifulSoup
from .data_structures import RiderStageResult, StageProfile


def parse_stage_results(soup: BeautifulSoup, race: str, year: int, stage_number: int) -> list[RiderStageResult]:
    """Parses the BeautifulSoup object of a stage results page and extracts structured data for each rider's result."""

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

        results.append(RiderStageResult(race, year, stage_number, rider, team, time, gap, rank, breakaway, breakaway_distance))

    return results


def parse_stage_profile(soup: BeautifulSoup, race: str, year: int, stage_number: int) -> StageProfile:
    """Parses the stage profile information (type and distance) from the BeautifulSoup object."""
    data = {}

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

    return StageProfile(race, year, stage_number, data.get("Date"), data.get("Start time"), winner_speed_kmh, data.get("Classification"), data.get("Race category"), distance_km, grad_final_km, data.get("ProfileScore"), data.get("Vertical meters"), data.get("Departure"), data.get("Arrival"), data.get("Won how"), temperature_c)
