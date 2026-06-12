from src.data.data_structures import StageURL, RiderStageResult, StageProfile
from src.data.parser import parse_stage_results, parse_stage_profile
from src.data.scraper import fetch_page


def test_parse_stage_results(test_Stage_url: StageURL = StageURL(race="giro", year=2026, stage_number=15, url="https://www.procyclingstats.com/race/giro-d-italia/2026/stage-15"), no_print: int = 5):
    """Tests the parse_stage_results function by fetching a known URL, parsing the stage results, and printing the first 5."""
    page_content = fetch_page(test_Stage_url.url)
    stage_results = parse_stage_results(test_Stage_url, page_content)
    print(f"Parsed {len(stage_results)} results:")
    for r in stage_results[:no_print]:
        print(r)


def test_parse_stage_profile(test_Stage_url: StageURL = StageURL(race="giro", year=2026, stage_number=15, url="https://www.procyclingstats.com/race/giro-d-italia/2026/stage-15")):
    """Tests the parse_stage_profile function by fetching a known URL, parsing the stage profile, and printing it."""
    page_content = fetch_page(test_Stage_url.url)
    stage_profile = parse_stage_profile(test_Stage_url, page_content)
    print(stage_profile)