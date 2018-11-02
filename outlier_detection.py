import math
from pprint import pprint

from sklearn.neighbors import LocalOutlierFactor
import pandas as pd

POSITIONS = ['TE', 'WR', 'QB', 'RB']


# Read the merged dataset and load in pandas data frame.
def load_data_to_be_processed():
    # data_set = pd.read_csv('cleaned_data/clean_historical_data.csv')
    data_set = pd.read_csv('cleaned_data/merged_data.csv')
    return data_set


# scikit earn requires a matrix of float numbers to detect outliers, thus we have to remove
# all the string values values before applying LOF
# this function remove the categorical values and remove the '%' from percentage attributes
def prepare_data_for_lof(data):
    # drop the first & second column of index
    data = data.drop(data.columns[1], axis=1)
    data = data.drop(data.columns[0], axis=1)
    data = data.drop(['game_date', 'opp', 'player', 'position', 'team'], axis=1)

    data['catch_pct'] = data['catch_pct'].map(lambda x: prepare_percent_field(x))

    data = data.drop(['home_team', 'away_team', 'kickoff_weather_summary_x', 'kickoff_wind_x'], axis=1)
    data['kickoff_cloud_cover_x'] = data['kickoff_cloud_cover_x'].map(lambda x: prepare_percent_field(x))
    data['kickoff_dome_x'] = data['kickoff_dome_x'].map(lambda x: '1' if 'Y' else '0')

    return data


# removes the '%' from the percentage fields.
def prepare_percent_field(x):
    if x is float:
        return 0
    x = str(x)
    return float(x.replace('%', ''))


# Removes all the NaN values form the dataset and replace with 0.
# (LOF doesn't seem to like NaNs)
def remove_all_zero_values(data):
    data = data.fillna(0)
    return data


# filter all rows not specific a given position
def filter_data_on_position(data, position):
    data = data[data['position'].map(lambda x: x) == position]
    return data


def main():
    for position in POSITIONS:
        print('------------------------')
        print('Position: ' + position)
        _data = load_data_to_be_processed()
        _data = filter_data_on_position(_data, position)
        _data = prepare_data_for_lof(_data)
        _data = remove_all_zero_values(_data)
        clf = LocalOutlierFactor(n_neighbors=20, contamination=0.00001)
        y_pred = clf.fit_predict(_data)
        inlier = 0
        outlier = 0
        for score in y_pred:
            if score == 1:
                inlier += 1
            else:
                outlier += 1

        print(inlier)
        print(outlier)
        outlier_p = outlier * 100.0 / (outlier + inlier)
        print('outlier percentage: ' + str(outlier_p))
        pprint(len(y_pred))
        pprint(y_pred)


if __name__ == '__main__':
    main()
