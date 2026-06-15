import pytest
from gt_stage_analysis.data.data_loading import StageURL, StageProfile, RiderStageResult
from gt_stage_analysis.data.data_loading import fetch_page, no_stages_in_year, url_builder, url_iterator, parse_stage_results, parse_stage_profile

#global variables for testing
base_url = "https://www.procyclingstats.com/race"

def test_no_stages_in_year():
    assert no_stages_in_year(base_url + "/vuelta-a-espana/1985") == 19
    assert no_stages_in_year(base_url + "/giro-d-italia/2025") == 21
    assert no_stages_in_year(base_url + "/tour-de-france/2006") == 20

def test_url_builder():
    assert type(url_builder(base_url, 'tour', 2021)[18]) == StageURL
    assert url_builder(base_url, 'giro', 2025)[0].url == 'https://www.procyclingstats.com/race/giro-d-italia/2025/stage-1'
    assert url_builder(base_url, 'vuelta', 2020)[5].url == 'https://www.procyclingstats.com/race/vuelta-a-espana/2020/stage-6'
    assert url_builder(base_url, 'tour', 2019)[20].url == 'https://www.procyclingstats.com/race/tour-de-france/2019/stage-21'

def test_url_iterator():
    url_list = url_iterator(base_url, 2024, 2025)
    assert type(url_list) == list
    assert type(url_list[0]) == StageURL
    assert url_list[0].race == 'GIRO'
    assert url_list[7].stage_number == 8
    assert url_list[20].race == 'GIRO'
    assert url_list[21].race == 'TOUR'
    assert url_list[23].stage_number == 3
    assert url_list[41].race == 'TOUR'
    assert url_list[42].race == 'VUELTA'
    assert url_list[50].stage_number == 9
    assert url_list[62].year == 2024
    assert url_list[63].year == 2025
    assert url_list[80].url == 'https://www.procyclingstats.com/race/giro-d-italia/2025/stage-18'

def test_parse_stage_profile():
    url = base_url + '/giro-d-italia/2026/stage-15'
    page_content = fetch_page(url)
    stage_url = StageURL('giro', 2026, 15, url)
    stage_profile = parse_stage_profile(stage_url, page_content)
    assert type(stage_profile) == StageProfile
    assert stage_profile.distance_km == 156
    assert stage_profile.year == 2026
    assert stage_profile.departure_location == 'Voghera'
    assert stage_profile.gradient_final_km == 0.8

def test_parse_stage_results():
    url = base_url + '/giro-d-italia/2026/stage-15'
    page_content = fetch_page(url)
    stage_url = StageURL('giro', 2026, 15, url)
    stage_results = parse_stage_results(stage_url, page_content)
    assert type(stage_results) == list
    assert type(stage_results[0]) == RiderStageResult
    assert stage_results[0].breakaway_distance == 153
    assert stage_results[0].rider_name == 'Dversnes Lavik Fredrik'