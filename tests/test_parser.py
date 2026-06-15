'''
OLD:
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

def test_url_builder(base_url: str = "https://www.procyclingstats.com/race/", race: str = "giro", year: int = 2026):
    """Tests the url_builder function by generating URLs for a specific race and year, printing the returned list."""
    url_list = url_builder(base_url, race, year)
    for stage_url in url_list:
        print(stage_url)

def test_url_iterator(base_url: str = "https://www.procyclingstats.com/race/", start_year: int = 2024, end_year: int = 2025):
    """Tests the url_iterator function by generating URLs for a range of years and printing the returned list."""
    url_list = url_iterator(base_url, start_year, end_year)
    for stage_url in url_list:
        print(stage_url)
'''