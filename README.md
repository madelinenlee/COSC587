COSC 587 semester long project

Data/
	clean_historical_data/
		using pro-football-reference.csv, cleaned data by filling in null values, etc
	clean_fantasy_data/
		using fantasy_data, cleaned data by filling in null values, etc


cleaning_score_fantasy.py
	This script defines functions to run a score on the fantasy dataset to determine how clean it is. this measures fraction of noisy values, missing values, etc. it outputs a percentage, and the lower percentage is better than a higher percentage.
	required packages:
		pandas
		numpy

cleaning_score_historical.py
	this script defines functions to run a score on the pro-football-reference dataset to determine how clean it is. it measures the fraction of noisy values, missing values, etc. it outputs a percentage, and a lower percentage is better than a higher percentage.
	required packages:
		pandas
		numpy

historical_data_cleaning.py
	this script defines functions to clean the pro-football-reference data and re-run the cleaning score. It then writes the newly cleaned dataset to a csv. (clean_historical_data.csv).
	required packages:
		pandas
		numpy
		csv
		import cleaning_score_historical

fantasy_data_cleaning.py
	this script defines functions to clean the fantasy data set and re-run the cleaning score. It then writes newly cleaned dataset to a csv. (clean_fantasy_data.csv)
	required packages:
		pandas
		numpy
		csv
		import cleaning_score_fantasy

Folder structure:
	all data is written into the same directory. cleaning_score_historical and historical_data_cleaning should be in the same directory. cleaning_score_fantasy and fantasy_data_cleaning should be in the same directory. 
	