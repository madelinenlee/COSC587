# COSC587
Semester Long Project
Website:
http://bigredskidoo.georgetown.domains/

cleaned_data/
	clean_fantasy_data.csv
		Cleaned version of 'data/fantasy-data.csv'

	clean_historical_data.csv
		Cleaned version of 'data/pro-football-reference.csv'
	
	weather_cleaned.csv
		Cleaned version of 'data/weather.csv'
	
	 merged_data.csv
	 	Merged version of foot_ball and weather data. 

data/
	fantasy_data/
		<POS>_<year>_wk<#>.csv
			Data pulled directly from www.fantasydata.com by position/season/week

	pro-football/
		<player>_<POS>.csv
			Data pulled directly from www.pro-football-reference.com by player

	fantasy-data.csv
		Consolidated data from 'data/fantasy_data/'

	pro-football-reference.csv
		Consolidated data from 'data/pro-football/'

	weather.csv
		Data pulled directly from www.NFLWeather.com
	
	team_latlong.xlsx
		Latitude/Longitude locations of where each team plays their games
	
		
clean_historical_quick.py
	This code is a first pass through of 'data/pro-football-reference.csv'. It limits data to seasons 2009 - 2017 and to offensive players.


cleaning_score_fantasy.py
	This script defines functions to run a score on 'data/fantasy-data.csv' to determine how clean it is. This measures fraction of noisy values,
	missing values, etc. It outputs a percentage, and the lower percentage is better than a higher percentage.

	Required Packages:
		csv
		numpy
		pandas
		pprint

	Required Folder Structure:
		This code requires your fantasy data to be saved in a 'data/' folder at the same level as this file with the name 'fantasy-data.csv'


cleaning_score_historical.py
	This script defines functions to run a score on 'data/pro-football-reference.csv' to determine how clean it is. It measures the fraction
	of noisy values, missing values, etc. It outputs a percentage, and a lower percentage is better than a higher percentage.

	Required Packages:
		csv
		numpy
		pandas
		pprint
		
	Required Folder Structure:
		This code requires your historical NFL data to be saved in a 'data/' folder at the same level as this file with the name 'pro-football-reference.csv'


fantasy_data.py

	This code scrapes projected player stats and projected fantasy points for all NFL players from the 2013 season to the 2017 season from
	www.fantasydata.com. A login/password is required. That data is saved as plain text in the code.
	
	Required Packages:
		csv
		itertools
		re
		time
		bs4
		selenium
		
	Required Inputs/Setup:
		Selenium requires a Chrome driver installed and a path to the executable to be specified at line 13 of the code.

	Required Folder Structure:
		This code requires a 'data/fantasy_data/' folder path to exist at the same level as this file.


fantasy_data_cleaning.py
	This script defines functions to clean 'data/fantasy_data.csv' and re-run the cleaning score. It then writes a newly cleaned
	dataset to a csv (clean_fantasy_data.csv).

	Required Packages:
		csv
		cleaning_score_fantasy
		numpy
		pandas
		pprint

	Required Folder Structure:
		This code requires your fantasy data to be saved in a 'data/' folder at the same level as this file with the name 'fantasy-data.csv'.
		It also requires your cleaning_score_fantasy.py code to be saved at the same level as this file.


historical_data_cleaning.py
	This script defines functions to clean 'data/pro-football-reference.csv' and re-run the cleaning score. It then writes the newly cleaned
	dataset to a csv (clean_historical_data.csv).

	Required Packages:
		csv
		cleaning_score_historical
		numpy
		pandas
		pprint

	Required Folder Structure:
		This code requires your historical NFL data to be saved in a 'data/' folder at the same level as this file with the name 'pro-football-reference.csv'.
		It also requires your cleaning_score_historical.py code to be saved at the same level as this file.


pro-football-reference.py

	This code scrapes all historical NFL player statistics from www.pro-football-reference.com.

	Required Packages:
		csv
		requests
		string
		time
		bs4

	Required Folder Structure:
		This code requires a 'data/pro-football/' folder path to exist at the same level as this file.


weather.py

	This code scrapes all available weather data for each NFL gam from the 2009 season to the 2017 season from www.NFLWeather.com. It will also
	pull weather the game was played in a dome or not.

	Required Packages:
		pandas
		requests

	Required Folder Structure:
		This code requires a 'data/' folder path to exist at the same level as this file.


weather_score_clean.py

	This code takes 'data/weather.csv' and calculates a score based on N/A values and noise. Then cleans the data, and recalculates the score.

	Required Packages:
		numpy
		pandas
		random
		pprint

	Required Folder Structure:
		This code requires your weather data to be saved in the 'data/' folder at the same level as this file with the name 'weather.csv'

Hp_test.py
	This script defines functions to run hypothesis testing on merged_data(Project 2)

	Required Packages:
		numpy
		pandas
		sklearn
		scikitplot
		matplotlib
		statsmodels.formula.api
 
 associations.py
 	This script defines association rules. (Project 2)

basic_stats_histo_corr.py
	This script shows basic stats and histograms of our dataset. (Project 2)
	
merge.py
	This script merges our weather and player data.(Project 2)

outlier_detection.py
	This script detects our outliers.(Project 2)
	
	
--------------------------------------------------------------------------------------------------------------------------------------
Project 3 Files

prediction
	This folder contains a script for our predictions making models. 

predictions
	This folder contains all the predition files. 

test_data
	
training_data

d3_map
	This folder is for our d3 plots
	bubble_chart_fantasy.html 
		Bubble chart for fantasy sports industry
	 
	 graph_weather.py
	 	Prepare the merge dataset for our d3 map plot. Calculates all the means for the weather. 
	
	index.html
		Map plot with location of the NFL teams and their weather overiew. 
		
	 map_graph.csv
	 	Data used in our map plot
		
	team_latlong.csv
		Data set of exact location of the NFL teams 
	
	us-states.json
		US states

mnl48_p3_d2.py
	This script creates plotly plots for our visualiztion. 
		
