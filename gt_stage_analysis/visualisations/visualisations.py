#-------------------------------------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from ..data.data_loading import GRAND_TOURS
from ..models.train import RandomForest, FEATURE_NAMES

#-------------------------------------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------------------------------------

COLOURS: dict[str, str] = {'giro': 'hotpink', 'tour': 'gold', 'vuelta': 'red', 'average': 'grey'}
LINESTYLES: dict[str, str] = {'giro': '-', 'tour': '-', 'vuelta': '-', 'average': '--'}

#-------------------------------------------------------------------------------------------------------------
# Functions to produce a plot showing the length of stages of a single year of all 3 Grand Tours
#-------------------------------------------------------------------------------------------------------------

def single_year_stage_length(data, year):
    #Call this function to extract the needed stage length data and the produce the plot
    if year not in range (data.start_year, data.end_year+1):
        raise ValueError("Selected year must be in the range of the data.")
    num_stages_dict = {}
    for key, value in GRAND_TOURS.items():
        data_key = f"{key}{year}"
        num_stages_dict[key] = data.num_stages_dict[data_key]
    stage_lengths, max_num_stages = extract_length(data, num_stages_dict)
    plot_stage_lengths(stage_lengths, max_num_stages, year)

def extract_length(data, num_stages_dict) -> tuple[dict[str, list], int]:
    '''
    Extracts the stage length data into three arrays that are returned inside a dictionary with the tour name as key, 
    the max_num_stages variable that is also returned is the maximum number of stages in any of the grand tours, to be 
    used in the x-axis length of the plot.
    '''
    sum_stages = 0
    giro_lengths = []
    tour_lengths = []
    vuelta_lengths = []
    for key, value in num_stages_dict.items():
        sum_stages+=value
    for num in range(0, sum_stages):
        if data.list_GT_stages[num].race == 'GIRO':
            giro_lengths.append(data.list_GT_stages[num].stage_profile.distance_km)
        elif data.list_GT_stages[num].race == 'TOUR':
            tour_lengths.append(data.list_GT_stages[num].stage_profile.distance_km)
        elif data.list_GT_stages[num].race == 'VUELTA':
            vuelta_lengths.append(data.list_GT_stages[num].stage_profile.distance_km)
    max_num_stages = max([len(giro_lengths), len(tour_lengths), len(vuelta_lengths)])
    return {'Giro': giro_lengths, 'Tour': tour_lengths, 'Vuelta': vuelta_lengths}, max_num_stages

def plot_stage_lengths(stage_lengths, max_num_stages, year):
    #Plotting function
    stages = np.arange(1, max_num_stages + 1)
    fig, ax = plt.subplots(figsize=(13, 5))

    for key, value in stage_lengths.items():
        ax.plot(stages, value, color=COLOURS[key.lower()], linewidth=1.4, alpha=0.6, zorder=2)
        ax.scatter(stages, value, label=key, color=COLOURS[key.lower()], s=40, zorder=3,
                   edgecolors='white', linewidths=0.5)

    ax.yaxis.grid(True, color='lightgrey', linewidth=0.7, zorder=1)
    ax.set_axisbelow(True)
    ax.xaxis.grid(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('lightgrey')
    ax.spines['bottom'].set_color('lightgrey')

    ax.set_title(f'Grand Tour Stage Lengths {year}', fontsize=11, color='black')
    ax.set_xlabel('Stage Number', fontsize=10, color='black')
    ax.set_ylabel('Stage Length/km', fontsize=10, color='black')
    ax.set_xticks(stages)
    ax.tick_params(axis='both', labelsize=9, colors='grey')


    legend = ax.legend(
        title='Grand Tour',
        title_fontsize=9,
        fontsize=9,
        loc='upper left',
        bbox_to_anchor=(1.01, 1),
        borderaxespad=0,
        frameon=True,
        framealpha=0.9,
        edgecolor='black',
    )
    legend.get_title().set_color('black')

    fig.tight_layout()
    plt.show()

#-------------------------------------------------------------------------------------------------------------
# Functions to show plots of the breakaway success rate over time.
#-------------------------------------------------------------------------------------------------------------

def breakaway_success_plot(df):
    breakaway_stats = (df.groupby(['race', 'year'])['break_success'].agg(total_stages='count',successful_breaks='sum').reset_index())
    breakaway_stats['success_rate_pct'] = (breakaway_stats['successful_breaks'] / breakaway_stats['total_stages'] * 100).round(2)
    pivot = breakaway_stats.pivot(index='year', columns='race', values='success_rate_pct')
    pivot['AVERAGE'] = pivot.mean(axis=1)

    fig, ax = plt.subplots(figsize=(12, 6))
    for col in ['GIRO', 'TOUR', 'VUELTA', 'AVERAGE']:
        if col in pivot.columns:
            ax.plot(
                pivot.index,
                pivot[col],
                label=col,
                color=COLOURS[col.lower()],
                linestyle=LINESTYLES[col.lower()],
                marker='o',
                markersize=4,
            )

    ax.set_title('Breakaway Success Rate by Grand Tour', fontsize=11, color='black')
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel('Breakaway Success Rate /%', fontsize=10)
    ax.set_xticks(pivot.index)
    ax.grid(True, linestyle='--', color='lightgrey')
    ax.set_ylim(0, 100)

    legend = ax.legend(
        title='Legend',
        title_fontsize=9,
        fontsize=9,
        loc='upper left',
        bbox_to_anchor=(1.01, 1),
        borderaxespad=0,
        frameon=True,
        framealpha=0.9,
        edgecolor='black',
    )
    legend.get_title().set_color('black')

    fig.tight_layout()
    plt.show()

#-------------------------------------------------------------------------------------------------------------
# Random Forest Plots
#-------------------------------------------------------------------------------------------------------------

def random_forest_conf_matrix_plot(forest: RandomForest):
    plt.figure(figsize=(8, 6))
    sns.heatmap(forest.conf_matrix, annot=True, fmt='g', cmap='Blues', cbar=False, 
                xticklabels=[True, False], yticklabels=[True, False])

    plt.title('Confusion Matrix for Random Forest Model')
    plt.xlabel('Predicted Breakaway Success')
    plt.ylabel('True Breakaway Success')
    plt.show()

def random_forest_feature_imp_plot(forest: RandomForest):
    plt.barh(FEATURE_NAMES, forest.feature_importances)
    plt.xlabel('Feature Importance')
    plt.title('Feature Importance in Random Forest Model')
    plt.show()