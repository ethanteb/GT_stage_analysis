from src.data.parser import parse_stage_results, parse_stage_profile
from src.data.scraper import fetch_page


def test_parse_stage_results(url: str = "https://www.procyclingstats.com/race/giro-d-italia/2026/stage-15"):
    """Tests the parse_stage_results function by fetching a known URL, parsing the stage results, and printing the first 5."""
    page_content = fetch_page(url)
    stage_results = parse_stage_results(page_content, "giro", 2026, 15)
    print(f"Parsed {len(stage_results)} results:")
    for r in stage_results[:5]:  # Print first 5 results
        print(r)

def test_parse_stage_profile(url: str = "https://www.procyclingstats.com/race/giro-d-italia/2026/stage-15"):
    """Tests the parse_stage_profile function by fetching a known URL, parsing the stage profile, and printing it."""
    page_content = fetch_page(url)
    stage_profile = parse_stage_profile(page_content, "giro", 2026, 15)
    print(stage_profile)