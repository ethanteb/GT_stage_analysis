#-------------------------------------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------------------------------------

from gt_stage_analysis import BASE_URL, GTResults, RandomForest
from gt_stage_analysis import (
    single_year_stage_length, breakaway_success_plot, 
    random_forest_conf_matrix_plot, random_forest_feature_imp_plot
    )
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
    
    results = GTResults.load_json(loc='data/raw/2020_2025_raw') # load data in from .json file
    
    #---------------------------------------------------------------------------------------------------------
    # Simple stage length plot
    #---------------------------------------------------------------------------------------------------------
    '''
    single_year_stage_length(data=results, year=2025) # plot stage lengths TODO: be able to select single year
    '''
    #---------------------------------------------------------------------------------------------------------
    # Extracting breakaway success rate data into a pandas dataframe, then plotting breakawy success rate
    #---------------------------------------------------------------------------------------------------------
    
    df = results.convert_to_breakaway_dataframe() # convert the race results into dataframe ready for analysis
    '''
    breakaway_success_plot(df) # plot breakaway success rate
    '''
    #---------------------------------------------------------------------------------------------------------
    # Data splitting then building random forest model
    #---------------------------------------------------------------------------------------------------------

    forest = RandomForest(df) # initiate class
    forest.train_test_split(test_size=0.2, random_state=42) # split data into training and testing sets
    forest.train_model(n_estimators=100, random_state=42) # train model
    forest.predict() # predict
    forest.eval() # evaluate using accuracy score metric

    #random_forest_conf_matrix_plot(forest) # plot confusion matrix #TODO: prettify
    random_forest_feature_imp_plot(forest) # plot feature importance #TODO: sort descending importance and prettify
