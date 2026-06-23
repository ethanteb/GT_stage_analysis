#-------------------------------------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------------------------------------

from gt_stage_analysis.data.data_loading import BASE_URL, GTResults
from gt_stage_analysis.visualisations.visualisations import single_year_stage_length

#-------------------------------------------------------------------------------------------------------------
# Main workflow
#-------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    #---------------------------------------------------------------------------------------------------------
    # Scraping & saving to .json file -> comment out when not required
    #---------------------------------------------------------------------------------------------------------
    '''
    results = GTResults(BASE_URL, 2025, 2025)
    results.build_stage_list()
    for stage in results.list_GT_stages:
        stage.fetch_page()
        stage.parse_stage_profile()
        stage.parse_stage_results()
    results.to_json('data/raw/2025_raw')
    '''
    #---------------------------------------------------------------------------------------------------------
    # Loading from .json -> comment out when not required
    #---------------------------------------------------------------------------------------------------------
    
    results = GTResults.load_json('data/raw/2025_raw')

    #---------------------------------------------------------------------------------------------------------
    # Simple stage length plot -> setup to produce a plot showing the stage lengths for 1 year of GTs
    #---------------------------------------------------------------------------------------------------------

    single_year_stage_length(results, 2025)
    