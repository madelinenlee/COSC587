import numpy as np
import pandas as pd

if __name__ == "__main__":

	hist_data = pd.read_csv(".\\cleaned_data\\clean_historical_data.csv")
	hist_data["game_pl_1"] = hist_data["game_num"] + 1 # bye week

	weather_data = pd.read_csv(".\\cleaned_data\\weather_cleaned.csv")
	weather_data = weather_data.groupby(["year", "season", "team_a", "team_b"]).min()

	merged_data = pd.merge(hist_data, weather_data,  how="left",
						   left_on=["year_id", "game_num", "home_team", "away_team"],
						   right_on=["year", "season", "team_b", "team_a"])
	
	merged_data = pd.merge(merged_data, weather_data,  how="left",
						   left_on=["year_id", "game_pl_1", "home_team", "away_team"],
						   right_on=["year", "season", "team_b", "team_a"])

		
	merged_data['kickoff_dome_x'].fillna(merged_data['kickoff_dome_y'],inplace=True)
	merged_data['kickoff_weather_summary_x'].fillna(merged_data['kickoff_weather_summary_y'],inplace=True)
	merged_data['kickoff_temperature_x'].fillna(merged_data['kickoff_temperature_y'],inplace=True)
	merged_data['kickoff_feels_like_x'].fillna(merged_data['kickoff_feels_like_y'],inplace=True)
	merged_data['kickoff_wind_x'].fillna(merged_data['kickoff_wind_y'],inplace=True)
	merged_data['kickoff_humidity_x'].fillna(merged_data['kickoff_humidity_y'],inplace=True)
	merged_data['kickoff_visibility_x'].fillna(merged_data['kickoff_visibility_y'],inplace=True)
	merged_data['kickoff_barometer_x'].fillna(merged_data['kickoff_barometer_y'],inplace=True)
	merged_data['kickoff_dew_point_x'].fillna(merged_data['kickoff_dew_point_y'],inplace=True)
	merged_data['kickoff_cloud_cover_x'].fillna(merged_data['kickoff_cloud_cover_y'],inplace=True)
	merged_data['kickoff_precipitation_prob_x'].fillna(merged_data['kickoff_precipitation_prob_y'],inplace=True)
	merged_data['q2_dome_x'].fillna(merged_data['q2_dome_y'],inplace=True)
	merged_data['q2_weather_summary_x'].fillna(merged_data['q2_weather_summary_y'],inplace=True)
	merged_data['q2_temperature_x'].fillna(merged_data['q2_temperature_y'],inplace=True)
	merged_data['q2_feels_like_x'].fillna(merged_data['q2_feels_like_y'],inplace=True)
	merged_data['q2_wind_x'].fillna(merged_data['q2_wind_y'],inplace=True)
	merged_data['q2_humidity_x'].fillna(merged_data['q2_humidity_y'],inplace=True)
	merged_data['q2_visibility_x'].fillna(merged_data['q2_visibility_y'],inplace=True)
	merged_data['q2_barometer_x'].fillna(merged_data['q2_barometer_y'],inplace=True)
	merged_data['q2_dew_point_x'].fillna(merged_data['q2_dew_point_y'],inplace=True)
	merged_data['q2_cloud_cover_x'].fillna(merged_data['q2_cloud_cover_y'],inplace=True)
	merged_data['q2_precipitation_prob_x'].fillna(merged_data['q2_precipitation_prob_y'],inplace=True)
	merged_data['q3_dome_x'].fillna(merged_data['q3_dome_y'],inplace=True)
	merged_data['q3_weather_summary_x'].fillna(merged_data['q3_weather_summary_y'],inplace=True)
	merged_data['q3_temperature_x'].fillna(merged_data['q3_temperature_y'],inplace=True)
	merged_data['q3_feels_like_x'].fillna(merged_data['q3_feels_like_y'],inplace=True)
	merged_data['q3_wind_x'].fillna(merged_data['q3_wind_y'],inplace=True)
	merged_data['q3_humidity_x'].fillna(merged_data['q3_humidity_y'],inplace=True)
	merged_data['q3_visibility_x'].fillna(merged_data['q3_visibility_y'],inplace=True)
	merged_data['q3_barometer_x'].fillna(merged_data['q3_barometer_y'],inplace=True)
	merged_data['q3_dew_point_x'].fillna(merged_data['q3_dew_point_y'],inplace=True)
	merged_data['q3_cloud_cover_x'].fillna(merged_data['q3_cloud_cover_y'],inplace=True)
	merged_data['q3_precipitation_prob_x'].fillna(merged_data['q3_precipitation_prob_y'],inplace=True)
	merged_data['q4_dome_x'].fillna(merged_data['q4_dome_y'],inplace=True)
	merged_data['q4_weather_summary_x'].fillna(merged_data['q4_weather_summary_y'],inplace=True)
	merged_data['q4_temperature_x'].fillna(merged_data['q4_temperature_y'],inplace=True)
	merged_data['q4_feels_like_x'].fillna(merged_data['q4_feels_like_y'],inplace=True)
	merged_data['q4_wind_x'].fillna(merged_data['q4_wind_y'],inplace=True)
	merged_data['q4_humidity_x'].fillna(merged_data['q4_humidity_y'],inplace=True)
	merged_data['q4_visibility_x'].fillna(merged_data['q4_visibility_y'],inplace=True)
	merged_data['q4_barometer_x'].fillna(merged_data['q4_barometer_y'],inplace=True)
	merged_data['q4_dew_point_x'].fillna(merged_data['q4_dew_point_y'],inplace=True)
	merged_data['q4_cloud_cover_x'].fillna(merged_data['q4_cloud_cover_y'],inplace=True)
	merged_data['q4_precipitation_prob_x'].fillna(merged_data['q4_precipitation_prob_y'],inplace=True)

	merged_data = merged_data.drop(['Unnamed: 0_y',
									 'Unnamed: 0',
									 'kickoff_precipitation_prob_x', # was always missing
									 'kickoff_dome_y',
									 'kickoff_weather_summary_y',
									 'kickoff_temperature_y',
									 'kickoff_feels_like_y',
									 'kickoff_wind_y',
									 'kickoff_humidity_y',
									 'kickoff_visibility_y',
									 'kickoff_barometer_y',
									 'kickoff_dew_point_y',
									 'kickoff_cloud_cover_y',
									 'kickoff_precipitation_prob_y',
									 'q2_dome_y',
									 'q2_weather_summary_y',
									 'q2_temperature_y',
									 'q2_feels_like_y',
									 'q2_wind_y',
									 'q2_humidity_y',
									 'q2_visibility_y',
									 'q2_barometer_y',
									 'q2_dew_point_y',
									 'q2_cloud_cover_y',
									 'q2_precipitation_prob_y',
									 'q3_dome_y',
									 'q3_weather_summary_y',
									 'q3_temperature_y',
									 'q3_feels_like_y',
									 'q3_wind_y',
									 'q3_humidity_y',
									 'q3_visibility_y',
									 'q3_barometer_y',
									 'q3_dew_point_y',
									 'q3_cloud_cover_y',
									 'q3_precipitation_prob_y',
									 'q4_dome_y',
									 'q4_weather_summary_y',
									 'q4_temperature_y',
									 'q4_feels_like_y',
									 'q4_wind_y',
									 'q4_humidity_y',
									 'q4_visibility_y',
									 'q4_barometer_y',
									 'q4_dew_point_y',
									 'q4_cloud_cover_y',
									 'q4_precipitation_prob_y',
									 'q2_dome_x',
									 'q2_weather_summary_x',
									 'q2_temperature_x',
									 'q2_feels_like_x',
									 'q2_wind_x',
									 'q2_humidity_x',
									 'q2_visibility_x',
									 'q2_barometer_x',
									 'q2_dew_point_x',
									 'q2_cloud_cover_x',
									 'q2_precipitation_prob_x',
									 'q3_dome_x',
									 'q3_weather_summary_x',
									 'q3_temperature_x',
									 'q3_feels_like_x',
									 'q3_wind_x',
									 'q3_humidity_x',
									 'q3_visibility_x',
									 'q3_barometer_x',
									 'q3_dew_point_x',
									 'q3_cloud_cover_x',
									 'q3_precipitation_prob_x',
									 'q4_dome_x',
									 'q4_weather_summary_x',
									 'q4_temperature_x',
									 'q4_feels_like_x',
									 'q4_wind_x',
									 'q4_humidity_x',
									 'q4_visibility_x',
									 'q4_barometer_x',
									 'q4_dew_point_x',
									 'q4_cloud_cover_x',
									 'q4_precipitation_prob_x'], axis=1)

	merged_data = merged_data[pd.notnull(merged_data["kickoff_dome_x"])]

	merged_data["position"] = merged_data["position"].replace("HB", "RB")
	merged_data["position"] = merged_data["position"].replace("FB", "RB")
	merged_data["position"] = merged_data["position"].replace("['LS', 'TE']", "TE")
	merged_data["position"] = merged_data["position"].replace("['WR', 'PR']", "WR")
	merged_data["position"] = merged_data["position"].replace("['FB', 'LB']", "RB")
	
	merged_data.to_csv(".\\cleaned_data\\merged_data.csv")
