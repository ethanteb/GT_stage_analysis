from src.data.scraper import fetch_page, no_stages_in_year, url_builder, url_iterator


def test_fetch_page(url: str = "https://www.procyclingstats.com/race/giro-d-italia/2026/stage-15"):
    """Tests the fetch_page scraper function by fetching a known URL and printing a portion of the HTML content."""
    page_content = fetch_page(url)
    print(page_content.prettify()[46500:46600]) # This portion of the HTML contains the start of the table of results


def test_no_stages_in_year(url: str = "https://www.procyclingstats.com/race/vuelta-a-espana/1985"):
    """Tests the no_stages_in_year function by fetching a known URL and printing the number of stages."""
    num_stages = no_stages_in_year(url)
    print(f"No. stages in specified year: {num_stages}") # Should print 19 for 1985 Vuelta


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