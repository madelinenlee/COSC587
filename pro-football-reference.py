import csv
import requests
import string
import time

from bs4 import BeautifulSoup


if __name__ == "__main__":

	base_url = "https://www.pro-football-reference.com"

	letters = string.ascii_uppercase # Define set of all capital letters (pro-football-reference requires capital letters in url)

	for letter in letters:
		url = "https://www.pro-football-reference.com/players/%s/" % letter
		r = requests.get(url)
		home_page = BeautifulSoup(r.content, "html.parser")

		# Get list of player names from the list
		table = home_page.find("div", {"id": "all_players"})
		body = table.find("div", {"id": "div_players"})
		players = body.find_all("p")

		for player in players:
			time.sleep(2)

			# Clean player name
			s = player.text
			pos = s[s.find("(")+1:s.find(")")]
			player_name = player.find("a").getText()
			clean_name = player_name.lower().replace(" ", "_")
			print(clean_name)

			# Go to player page
			href = player.find("a")["href"]
			player_url = "%s%s" % (base_url, href)
			r = requests.get(player_url)
			player_page = BeautifulSoup(r.content, "html5lib")

			try: # Sometimes there's just no data and this breaks

				# Go to Gamelogs -> Career page
				section = player_page.find("div", {"id":"inner_nav"})
				bar = section.find("ul", {"class": "hoversmooth"})
				game_logs = bar.find_all("li")[1]
				if game_logs.find("a").text != "Gamelogs": continue # If player has no data, skip
				career = game_logs.find("ul").findAll("li")[0]
				career_url = career.find("a").get("href")
				game_url = "%s%s" % (base_url, career_url)
				r = requests.get(game_url)
				game_page = BeautifulSoup(r.content, "html5lib")

				with open("data\\pro-football\\game_data\\%s_%s.csv" % (clean_name, pos), "w+") as ofile:
					csv_ofile = csv.writer(ofile, lineterminator="\n")

					# Get player stats per game
					all_stats = game_page.find("div", {"id": "all_stats"})

					# Get attributes from header
					header = all_stats.find("thead").findAll("tr")[1]
					cols = header.findAll("th")
					head = []

					for col in cols:
						head.append(col.get("data-stat"))

					csv_ofile.writerow(head)

					# Get data from table
					body = all_stats.find("tbody")
					rows = body.findAll("tr")

					for row in rows:
						if row.get("id"): # If this row has an id attribute (has stats)
							cols = row.findAll(["th", "td"])
							record = []

							for col in cols:
								record.append(col.text)

							if record: csv_ofile.writerow(record) # Only print to file if data exists (mid table headers)

			except:
				pass