#-------------------------------------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------------------------------------

from gt_stage_analysis import BASE_URL, GTResults
from gt_stage_analysis import single_year_stage_length, breakaway_success_plot
import pandas as pd

#-------------------------------------------------------------------------------------------------------------
# Main workflow
#-------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    #---------------------------------------------------------------------------------------------------------
    # Scraping & saving to .json file -> comment out when not required
    #---------------------------------------------------------------------------------------------------------
    '''
    results = GTResults(base_url=BASE_URL, start_year=2020, end_year=2025)
    results.build_stage_list()
    for stage in results.list_GT_stages:
        stage.fetch_page()
        stage.parse_stage_profile()
        stage.parse_stage_results()
    results.to_json(loc='data/raw/2020_2025_raw')
    '''
    #---------------------------------------------------------------------------------------------------------
    # Loading from .json -> comment out when not required
    #---------------------------------------------------------------------------------------------------------
    
    results = GTResults.load_json(loc='data/raw/2020_2025_raw')
    
    #---------------------------------------------------------------------------------------------------------
    # Simple stage length plot -> setup to produce a plot showing the stage lengths for 1 year of GTs
    #---------------------------------------------------------------------------------------------------------
    '''
    single_year_stage_length(data=results, year=2025)
    '''
    #---------------------------------------------------------------------------------------------------------
    # Extracting breakaway success rate data into a pandas dataframe, then plotting breakawy success rate
    #---------------------------------------------------------------------------------------------------------
    
    df = results.convert_to_breakaway_dataframe()
    breakaway_success_plot(df)
    