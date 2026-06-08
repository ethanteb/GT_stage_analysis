from src.data.scraper import fetch_page
from src.data.parser import parse_stage_results

def test_scrape_gt():
    url = "https://www.procyclingstats.com/race/giro-d-italia/2026/stage-15"
    page_content = fetch_page(url)
    print(page_content.prettify()[45000:50000])

def test_parse_stage_results():
    url = "https://www.procyclingstats.com/race/giro-d-italia/2026/stage-15"
    page_content = fetch_page(url)
    results = parse_stage_results(page_content, "giro", 2026, 15)
    print(f"Parsed {len(results)} results:")
    for r in results[:5]:  # Print first 5 results
        print(r)

if __name__ == "__main__":
    #test_scrape_gt()
    test_parse_stage_results()