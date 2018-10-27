
# coding: utf-8

# In[174]:


import numpy as np
import pandas as pd
import random
from pprint import  pprint


def read_file_to_pandas(filename):
    myDataFrame = pd.read_csv(filename , sep=',', encoding='latin1')
    return myDataFrame

def replace_blank_na_with_nan(df):
    df.replace("NA", np.NaN)
    df.replace(r'\s+', np.nan, regex=True)
    return df
    
def get_percentage_missing_in_column(df):
    percent_missing = df.isnull().sum() * 100 / len(df)
    percent_missing = percent_missing.sort_values(ascending=False)
    return percent_missing
    #we have mostly missing values in the later quaters columns. We decided to leave it there for now and not cleaning those

def get_percentage_noise_in_column():
    vals = []
    vals.append(df[(df["year"] < 2013) | (df["year"] > 2018) ].shape[0])
    vals.append(df[ (df["season"]<1) | (df["season"] > 17) ].shape[0])
    vals.append(df[ (~df["team_a"].isin(unique_team_list))].shape[0])
    vals.append(df[(~df["team_b"].isin(unique_team_list))].shape[0])
    vals.append(df[(~df["kickoff_dome"].isin(["N", "Y"]))].shape[0])
    vals.append(df[(df["kickoff_humidity"] < 0) | (df["kickoff_humidity"] > 100)].shape[0])
    vals.append(df[df["kickoff_visibility"] <= 0].shape[0])
    vals.append(df[(df["kickoff_barometer"] < 20) | (df["kickoff_barometer"] > 40)].shape[0])
    vals.append(df[(df["kickoff_dew_point"] < -60) | (df["kickoff_dew_point"] > 150)].shape[0])

    keys = ["year", "season","team_a", "team_b", "kickoff_dome", "kickoff_humidity"
            ,"kickoff_visibility", "kickoff_barometer" ,"kickoff_dew_point"]
    new_vals = convert_to_percentage(vals)
    noise_series = pd.Series(new_vals, index= keys)
    return noise_series

"""Helper for coverting values to percentage"""
def convert_to_percentage(vals):
    result = []
    for val in vals:
        val = val * 100 / len(df)
        result.append(val)
    return result

#calculate score by (1- two percetages/2)* 100. 
def calculate_score(unique_team_list):
    na_percentage_series = get_percentage_missing_in_column(df) 
    # filter out the series that have too much missing data
    na_percentage_series = na_percentage_series[na_percentage_series < 35 ]
    noise_percentage_series = get_percentage_noise_in_column()
    #combing two series and calculate score 
    score_df = pd.concat([na_percentage_series, noise_percentage_series], axis=1).reset_index()
    score_df = score_df.fillna(0)
    score_df["score"] = 100 - (score_df[0]+score_df[1])/2
    # sort the score 
    score_df = score_df.sort_values(by=["score"])
    pprint(score_df)

def remove_measure_unit(col_list):
    for col in col_list:
        df[col] = df[col].str.extract('(\d+)', expand=False)
        df[col] =  pd.to_numeric(df[col], errors =  "coerce")

#Cleaning the data 

def clean():
    df["kickoff_barometer"] = df["kickoff_barometer"].apply(replace_with_barometer)
    df["kickoff_visibility"] =  df["kickoff_visibility"].apply(replace_with_visibility)

def replace_with_barometer(barometer):
    if barometer < 20 or barometer > 40 or np.isnan(barometer):
        new_barometer = random.randint(29,32)
        return new_barometer
    else:
        return barometer

def replace_with_visibility(visibility):
    if  np.isnan(visibility) or visibility == 0:
        new_visibility = random.randint(1,50)
        return new_visibility
    else:
        return visibility

#not in use for now 
def fill_kickoff_weather_with_other_api():
    #find the city with missing kickoff_weather
    nan_rows = df[df["kickoff_weather_summary"].isnull()]
    home_teams = pd.unique(nan_rows["team_b"].ravel())
#     fill_kickoff_weather_with_other_api(df)
#     api_key = '1e0b837611b9488aa385c9630276b93e'
#     weather = Api(api_key)    
    
def main():    
    remove_measure_unit(["kickoff_visibility","kickoff_barometer","kickoff_dew_point","kickoff_humidity"])
    #score before cleaning
    calculate_score(unique_team_list) 
    clean()
    #score after cleaning 
    calculate_score(unique_team_list)

if __name__ == "__main__":
    unique_team_list = ['BUF', 'NYJ', 'CLE', 'PIT', 'IND', 'JAX', 'DEN', 'LAC', 'DAL', 'WAS', 
                        'CHI', 'DET', 'CAR', 'NO', 'SF', 'LAR', 'NYG',
                        'BAL', 'TEN', 'GB', 'MIN', 'TB', 'ATL', 'ARI', 'MIA',
                        'CIN', 'HOU', 'PHI', 'SEA', 'NE', 'KC', 'OAK']
    df = read_file_to_pandas("data\\weather.csv")
    df = replace_blank_na_with_nan(df)
    main()

