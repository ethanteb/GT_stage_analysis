#-------------------------------------------------------------------------------------------------------------
# Imports, including functions, classes & methods to be tested
#-------------------------------------------------------------------------------------------------------------

import pytest, requests, time
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from gt_stage_analysis import (
    _parse_float, _parse_int, fetch_page,
    StageProfile, RiderStageResult, GTStage, GTResults,
    BASE_URL, GRAND_TOURS
)

#-------------------------------------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------------------------------------

#Taken from 2026 giro stage 15
PROFILE_HTML = """
<html><body>
  <ul>
    <li class=""><div class="title ">Date:  </div><div class=" value" >24 May 2026</div></li>
    <li><div class="title ">Start time: </div><div class=" value" >13:55 </div></li>
    <li><div class="title ">Avg. speed winner: </div><div class=" value" >51.064 km/h</div></li>
    <li><div class="title ">Classification: </div><div class=" value" >2.UWT</div></li>
    <li><div class="title ">Race category: </div><div class=" value" >ME - Men Elite</div></li>
    <li><div class="title ">Distance: </div><div class=" value" >156 km</div></li>
    <li><div class="title ">Points scale: </div><div class=" value" ><a  href="info.php?s=point-scales&season=2026&category=1&scale=8">GT.B.Stage</a></div></li>
    <li><div class="title ">UCI scale: </div><div class=" value" ><a  href="info.php?s=point-scales&season=2026&category=1&scale=9863">UCI.WR.GT.B.Stage</a></div></li>
    <li><div class="title ">Parcours type: </div><div class=" value" ><span class="icon profile p1 mg_rp4 "></span></div></li>
    <li><div class="title ">Gradient final km: </div><div class=" value" >0.8%</div></li>
    <li><div class="title ">ProfileScore: </div><div class=" value" >7</div></li>
    <li><div class="title ">Vertical meters: </div><div class=" value" >612</div></li>
    <li><div class="title ">Departure: </div><div class=" value" ><a  href="location/voghera">Voghera</a></div></li>
    <li><div class="title ">Arrival: </div><div class=" value" ><a  href="location/milan">Milan</a></div></li>
    <li><div class="title ">Race ranking: </div><div class=" value" ><a  href="rankings/me/races">4</a></div></li>
    <li><div class="title ">Startlist quality score: </div><div class=" value" ><a  href="race/giro-d-italia/2026/startlist/startlist-quality">955 (760)</a></div></li>
    <li><div class="title ">Won how: </div><div class=" value" >Sprint of 4 riders</div></li>
    <li><div class="title ">Avg. temperature: </div><div class=" value" ><a  href="race/giro-d-italia/2026/results/hottest-stages">30 °C</a></div></li>
    <li><div class="title ">Timelimit: </div><div class=" value" >10%, or 3:22:18 (+0:19:00)</div></li>
  </ul>
</body></html>
"""

RESULTS_HTML = """
<html><body>
  <div id="resultsCont">
    <table class="results">
      <tbody>
        <tr><td>1</td><td class="fs11 clr666 " >107</td><td class="fs11 clr666 " >+2:41:57</td><td class="bibs " >215</td><td class="h2h " ><input type="checkbox" class="gotoH2H" style="margin: 0; float: left; " /><div class="clear"></div></td><td class="specialty " ><div class="resSp bg green"></div><span class="fs10 clr999">Classic</span></td><td class="age " >29</td><td class="ridername " ><div class="cont"><span translate="no"><span class="flag no"></span> <a data-ct="EU" href="rider/fredrik-dversnes"><span class="uppercase">Dversnes Lavik</span> Fredrik</a> <div title="153 kilometre in a group in front of the peloton" class="svg_shield"></div><div class="clear"></div><div class="showIfMobile fs12 clr999" >Uno-X Mobility</div></span></div></td><td class="cu600 " ><a data-bc="1" href="team/uno-x-mobility-2026">Uno-X Mobility</a></td><td class="uci_pnt " >180</td><td class="pnt " >80</td><td class="ar cu600 " ><font class="blue fs11">16″</font></td><td class="time ar " ><font>3:03:18</font><span class="hide">3:03:18</span></td></tr>
        <tr><td>2</td><td class="fs11 clr666 " >96</td><td class="fs11 clr666 " >+2:31:40</td><td class="bibs " >164</td><td class="h2h " ><input type="checkbox" class="gotoH2H" style="margin: 0; float: left; " /><div class="clear"></div></td><td class="specialty " ><div class="resSp bg pink"></div><span class="fs10 clr999">Hills</span></td><td class="age " >34</td><td class="ridername " ><div class="cont"><span translate="no"><span class="flag it"></span> <a data-ct="EU" href="rider/mirco-maestri"><span class="uppercase">Maestri</span> Mirco</a> <div title="149 kilometre in a group in front of the peloton" class="svg_shield"></div><div class="clear"></div><div class="showIfMobile fs12 clr999" >Team Polti VisitMalta</div></span></div></td><td class="cu600 " ><a data-bc="2" href="team/team-polti-visitmalta-2026">Team Polti VisitMalta</a></td><td class="uci_pnt " >130</td><td class="pnt " >50</td><td class="ar cu600 " ><font class="blue fs11">8″</font></td><td class="time ar " ><font>,,</font><span class="hide">0:00</span></td></tr>
      </tbody>
    </table>
  </div>
</body></html>
"""

@pytest.fixture
def profile_soup():
    return BeautifulSoup(PROFILE_HTML, "html.parser")

@pytest.fixture
def results_soup():
    return BeautifulSoup(RESULTS_HTML, "html.parser")

@pytest.fixture
def sample_profile(): #fix this to match sample return
    return StageProfile(
        race= "GIRO",
        year= 2026,
        stage_number= 15,
        date= "24 May 2026",
        start_time= "13:55",
        avg_speed_winner_kmh= 51.064,
        classification= "2.UWT",
        race_category= "ME - Men Elite",
        distance_km= 156.0,
        gradient_final_km= 0.8,
        profile_score= 7,
        vertical_metres= 612,
        departure_location= "Voghera",
        arrival_location= "Milan",
        race_ranking= 4,
        won_how= "Sprint of 4 riders",
        avg_temperature_c= 30.0
    )

@pytest.fixture
def sample_result():
    return RiderStageResult(
        race= "GIRO",
        year= 2026,
        stage_number= 15,
        rider_name= "Dversnes Lavik Fredrik",
        team= "Uno-X Mobility",
        time= "3:03:18",
        gap= "+2:41:57",
        rank= 1,
        breakaway_distance= 153
    )

@pytest.fixture
def gt_stage_with_content(profile_soup):
    """A GTStage with page_content pre-loaded"""
    stage = GTStage("giro", 2026, 15, "http://fake-url/stage-15")
    stage.page_content = profile_soup
    return stage

@pytest.fixture
def populated_gt_results(sample_profile, sample_result):
    """A GTResults object pre-populated with one stage."""
    results = GTResults(BASE_URL, 2026, 2026)
    stage = GTStage.from_dict({
        "race": "GIRO", "year": 2026, "stage_number": 15,
        "url": "http://fake-url/stage-15",
        "stage_profile": sample_profile.to_dict(),
        "stage_results": [sample_result.to_dict()],
    })
    results.list_GT_stages = [stage]
    results.num_stages_dict = {"giro2026": 21}
    return results

#-------------------------------------------------------------------------------------------------------------
# Helpers
#-------------------------------------------------------------------------------------------------------------

class TestHelpers:
    def test_parse_float_basic(self):
        assert _parse_float("51.064 km/h", r"(-?\d+(?:\.\d+)?)\s*km/h") == 51.064

    def test_parse_float_no_match(self):
        assert _parse_float("no numbers present", r"(-?\d+(?:\.\d+)?)\s*km/h") is None

    def test_parse_float_none_input(self):
        assert _parse_float(None, r"(-?\d+(?:\.\d+)?)") is None

    def test_parse_float_negative(self):
        assert _parse_float("-3.5 %", r"(-?\d+(?:\.\d+)?)\s*%") == -3.5

    def test_parse_int_basic(self):
        assert _parse_int("18 °C", r"(-?\d+)\s*°C") == 18

    def test_parse_int_no_match(self):
        assert _parse_int("word not number", r"(-?\d+)\s*°C") is None

    def test_parse_int_none_input(self):
        assert _parse_int(None, r"(-?\d+)") is None


#-------------------------------------------------------------------------------------------------------------
# Test StageProfile dataclass
#-------------------------------------------------------------------------------------------------------------

class TestStageProfile:
    def test_to_dict_keys(self, sample_profile):
        d = sample_profile.to_dict()
        assert set(d.keys()) == {
            "race",
            "year",
            "stage_number",
            "date",
            "start_time",
            "avg_speed_winner_kmh",
            "classification",
            "race_category",
            "distance_km",
            "gradient_final_km",
            "profile_score",
            "vertical_metres",
            "departure_location",
            "arrival_location",
            "race_ranking",
            "won_how",
            "avg_temperature_c"
        }

    def test_round_trip(self, sample_profile):
        assert StageProfile.from_dict(sample_profile.to_dict()) == sample_profile

    def test_str_contains_key_info(self, sample_profile):
        s = str(sample_profile)
        assert "GIRO" in s and "2026" in s and "Stage 15" in s

    def test_none_fields_survive_round_trip(self):
        profile = StageProfile(
            race="TOUR", year=2023, stage_number=1, date=None, start_time=None,
            avg_speed_winner_kmh=None, classification=None, race_category=None,
            distance_km=None, gradient_final_km=None, profile_score=None,
            vertical_metres=None, departure_location=None, arrival_location=None,
            race_ranking=None, won_how=None, avg_temperature_c=None,
        )
        assert StageProfile.from_dict(profile.to_dict()) == profile


#-------------------------------------------------------------------------------------------------------------
# Test RiderStageResult dataclass
#-------------------------------------------------------------------------------------------------------------

class TestRiderStageResult:
    def test_round_trip(self, sample_result):
        assert RiderStageResult.from_dict(sample_result.to_dict()) == sample_result

    def test_str_non_winner_shows_gap(self, sample_result):
        sample_result.gap = "+1:23"
        sample_result.rank = 2
        assert "+1:23" in str(sample_result)

    def test_str_shows_breakaway_distance(self, sample_result):
        sample_result.breakaway_distance = 40
        assert "40" in str(sample_result)


#-------------------------------------------------------------------------------------------------------------
# Test FetchPage
#-------------------------------------------------------------------------------------------------------------

class TestFetchPage:
    @patch("time.sleep")
    @patch("requests.get")
    def test_returns_beautifulsoup(self, mock_get, mock_sleep):
        mock_get.return_value = MagicMock(
            status_code=200, text="<html><body><h1>Hello</h1></body></html>"
        )
        mock_get.return_value.raise_for_status = MagicMock()
        result = fetch_page("http://example.com")
        assert isinstance(result, BeautifulSoup)
        assert result.find("h1").text == "Hello"

    @patch("time.sleep")
    @patch("requests.get")
    def test_respects_delay(self, mock_get, mock_sleep):
        mock_get.return_value = MagicMock(text="<html/>")
        mock_get.return_value.raise_for_status = MagicMock()
        fetch_page("http://example.com", delay=2.0)
        mock_sleep.assert_called_once_with(2.0)

    @patch("time.sleep")
    @patch("requests.get")
    def test_request_error_returns_fallback_soup(self, mock_get, mock_sleep):
        mock_get.side_effect = requests.RequestException("timeout")
        result = fetch_page("http://example.com")
        assert isinstance(result, BeautifulSoup)
        assert "Error" in result.get_text()


#-------------------------------------------------------------------------------------------------------------
# Test GTStage Parsing
#-------------------------------------------------------------------------------------------------------------

class TestGTStageParsing:
    def test_require_page_raises_before_fetch(self):
        stage = GTStage("giro", 2026, 15, "http://fake")
        stage.stage_profile = sample_profile
        stage.stage_results = sample_result
        stage.page_content = None
        with pytest.raises(RuntimeError, match="fetch_page"):
            stage._require_page()

    def test_parse_stage_profile_populates(self, gt_stage_with_content):
        gt_stage_with_content.parse_stage_profile()
        p = gt_stage_with_content.stage_profile
        assert p is not None
        assert p.distance_km == 156.0
        assert p.avg_speed_winner_kmh == 51.064
        assert p.departure_location == "Voghera"
        assert p.avg_temperature_c == 30

    def test_parse_stage_results_populates(self):
        stage = GTStage("giro", 2026, 15, "http://fake")
        stage.page_content = BeautifulSoup(RESULTS_HTML, "html.parser")
        stage.parse_stage_results()
        assert len(stage.stage_results) == 2
        assert stage.stage_results[0].rider_name == "Dversnes Lavik Fredrik"
        assert stage.stage_results[0].rank == 1
        assert stage.stage_results[0].gap == "+2:41:57"
        assert stage.stage_results[1].rank == 2
        assert stage.stage_results[1].breakaway_distance == 149

    def test_parse_results_missing_table(self, gt_stage_with_content):
        # profile_soup has no results table — should not raise
        gt_stage_with_content.stage_profile = sample_profile
        gt_stage_with_content.stage_results = sample_result
        gt_stage_with_content.parse_stage_results()
        # stage_results is unchanged (not set, or empty)

    def test_parse_rider_name_no_td(self):
        assert GTStage._parse_rider_name(None) == ""

    def test_parse_breakaway_no_shield(self):
        soup = BeautifulSoup('<td class="ridername"><a href="#"><span class="uppercase">TEST</span></a></td>', "html.parser")
        td = soup.find("td", class_="ridername")
        assert GTStage._parse_breakaway(td) is None


#-------------------------------------------------------------------------------------------------------------
# Test GTStage IO
#-------------------------------------------------------------------------------------------------------------

class TestGTStageIO:
    def test_round_trip_with_profile_and_results(self, sample_profile, sample_result):
        stage = GTStage("giro", 2024, 15, "http://fake")
        stage.stage_profile = sample_profile
        stage.stage_results = [sample_result]
        restored = GTStage.from_dict(stage.to_dict())
        assert restored.race == "GIRO"
        assert restored.stage_profile == sample_profile
        assert restored.stage_results[0] == sample_result


#-------------------------------------------------------------------------------------------------------------
# Test GTResults IO
#-------------------------------------------------------------------------------------------------------------

class TestGTResultsIO:
    def test_round_trip_in_memory(self, populated_gt_results):
        restored = GTResults.from_dict(populated_gt_results.to_dict())
        assert restored.start_year == 2026
        assert len(restored.list_GT_stages) == 1
        assert restored.num_stages_dict == {"giro2026": 21}

    def test_json_round_trip(self, populated_gt_results, tmp_path):
        loc = str(tmp_path / "test_data")
        populated_gt_results.to_json(loc)
        restored = GTResults.load_json(loc)
        assert len(restored.list_GT_stages) == 1
        assert restored.list_GT_stages[0].year == 2026

    def test_str_output(self, populated_gt_results):
        s = str(populated_gt_results)
        assert "2026" in s and "stages_loaded=1" in s


#-------------------------------------------------------------------------------------------------------------
# Test GTResults Build
#-------------------------------------------------------------------------------------------------------------

class TestGTResultsBuild:
    @patch("gt_stage_analysis.fetch_page")
    def test_build_stage_list_correct_count(self, mock_fetch):
        mock_soup = BeautifulSoup(
            '<div class="title-line2">21 Stages</div>', "html.parser"
        )
        mock_fetch.return_value = mock_soup
        results = GTResults(BASE_URL, 2026, 2026)
        results.num_stages_dict = {"giro2026": 21, "tour2026": 21, "vuelta2026": 21}
        results.build_stage_list()
        assert len(results.list_GT_stages) == 63 #3 grand tours with 21 stages each => 63 total stages

    @patch("gt_stage_analysis.fetch_page")
    def test_build_stage_list_url_format(self, mock_fetch):
        mock_fetch.return_value = BeautifulSoup(
            '<div class="title-line2">5 Stages</div>', "html.parser"
        )
        results = GTResults(BASE_URL, 2026, 2026)
        results.num_stages_dict = {"giro2026": 21, "tour2026": 21, "vuelta2026": 21}
        results.build_stage_list()
        urls = [s.url for s in results.list_GT_stages]
        assert any("giro-d-italia/2026/stage-15" in u for u in urls)

    @patch("gt_stage_analysis.fetch_page")
    def test_num_stages_dict_keys(self, mock_fetch):
        mock_fetch.return_value = BeautifulSoup(
            '<div class="title-line2">3 Stages</div>', "html.parser"
        )
        results = GTResults(BASE_URL, 2026, 2026)
        results.num_stages_dict = {"giro2026": 21, "tour2026": 21, "vuelta2026": 21}
        results.build_stage_list()
        for short in GRAND_TOURS:
            assert f"{short}2026" in results.num_stages_dict


#-------------------------------------------------------------------------------------------------------------
# Test Breakaway DataFrame
#-------------------------------------------------------------------------------------------------------------

class TestBreakawayDataframe:
    def test_columns_include_break_success(self, populated_gt_results):
        df = populated_gt_results.convert_to_breakaway_dataframe()
        assert "break_success" in df.columns

    def test_breakaway_winner_is_true(self, sample_profile):
        result_with_break = RiderStageResult(
            race="GIRO", year=2026, stage_number=15,
            rider_name="BREAKAWAY Rider", team="Some Team",
            time="4:30:00", gap=None, rank=1, breakaway_distance=40,
        )
        results = GTResults(BASE_URL, 2026, 2026)
        stage = GTStage("giro", 2026, 15, "http://fake")
        stage.stage_profile = sample_profile
        stage.stage_results = [result_with_break]
        results.list_GT_stages = [stage]
        df = results.convert_to_breakaway_dataframe()
        assert df["break_success"].iloc[0]

    def test_index_error_resilience(self, sample_profile):
        """Stages with empty results lists (e.g. TTT) should not raise."""
        results = GTResults(BASE_URL, 2026, 2026)
        stage = GTStage("giro", 2026, 15, "http://fake")
        stage.stage_profile = sample_profile
        stage.stage_results = []
        results.list_GT_stages = [stage]
        df = results.convert_to_breakaway_dataframe()
        assert not df["break_success"].iloc[0]