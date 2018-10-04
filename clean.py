import numpy as np
import pandas as pd


def cleanProFootballReference(df):

	# Only keep offensive positions
	off_pos = "QB|WR|RB|TE|K|FB|HB"
	df = df[df.position.str.contains(off_pos, na=False)]

	# Narrow data to games since 2009 not including 2018 games
	df = df[2009 <= df.year_id]
	df = df[df.year_id <= 2017]
	
	# Remove unnecessary columns (defensive / punting)
	df = df.drop(["def_int", "def_int_yds", "game_result", "punt",
		          "punt_blocked", "punt_yds", "sacks", "safety_md",
		          "tackles_assists", "tackles_solo",], axis=1)

	# Switch game_location = "@" to a flag for 'away' column
	df["away"] = np.where(df["game_location"] == "@", 1, 0)
	df = df.drop("game_location", axis=1)	

	return df


if __name__ == "__main__":

	# Pro Football Reference
	filename = "data\\pro-football-reference.csv"
	pfr = pd.read_csv(filename)

	pfr = cleanProFootballReference(pfr)

	pfr.to_csv("cleaned_data\\pro-football-reference.csv", index=False)

	