from src.data.scraper import fetch_page, url_builder
from src.data.parser import parse_stage_results, parse_stage_profile

def test_scrape_gt(url):
    page_content = fetch_page(url)
    print(page_content.prettify()[45000:50000])

def test_parse_stage_results(url):
    page_content = fetch_page(url)
    stage_results = parse_stage_results(page_content, "giro", 2026, 15)
    print(f"Parsed {len(stage_results)} results:")
    for r in stage_results[:5]:  # Print first 5 results
        print(r)

def test_parse_stage_profile(url):
    page_content = fetch_page(url)
    stage_profile = parse_stage_profile(page_content, "giro", 2026, 15)
    print(stage_profile)

if __name__ == "__main__":
    #url = "https://www.procyclingstats.com/race/giro-d-italia/2026/stage-15"
    base_url = "https://www.procyclingstats.com/race/"
    url = url_builder(base_url, "giro", 2026, 21)

    #test_scrape_gt(url)
    #test_parse_stage_results(url)
    test_parse_stage_profile(url)
