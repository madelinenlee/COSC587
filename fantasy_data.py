import csv
import itertools
import re
import time

from selenium import webdriver
from bs4 import BeautifulSoup


if __name__ == "__main__":

	# Need a driver to produce html from javascript
	driver = webdriver.Chrome(executable_path="C:\\Program Files\\chromedriver\\chromedriver")

	# Login
	login_url = "https://fantasydata.com/user/login"
	driver.get(login_url)
	time.sleep(5)
	email = driver.find_element_by_id("Email")
	email.send_keys("tspaightm@gmail.com") # Input email address
	password = driver.find_element_by_id("Password")
	password.send_keys("Griffey1!") # Input password
	driver.find_element_by_class_name("submit-button").click() # Click button

	time.sleep(2) # Allow page to login. Takes a second.

	base_url = "https://fantasydata.com/nfl-stats/fantasy-football-weekly-projections"
	seasons = range(2013, 2017 + 1)
	weeks = range(1, 17 + 1)
	positions = range(2, 7 + 1)
	pos = [None, None, "QB", "RB", "WR", "TE", "K", "DST"]

	for [s, w, p] in list(itertools.product(seasons, weeks, positions)): # Loop through all combinations of season, week, and position
		time.sleep(10)
		url = "%s?season=%s&startweek=%s&endweek=%s&position=%s" % (base_url, s, w, w, p)
		driver.get(url)
		driver.find_element_by_css_selector("a[ng-click='SetPageSize(300);']").click() # Set display limit to 300 records
		time.sleep(2)
		table = driver.find_element_by_class_name("stats-grid-container")
		html = table.get_attribute("innerHTML")

		with open("data\\fantasy_data\\%s_%s_wk%s.csv" % (pos[p], s, w), "w+") as ofile:
			csv_ofile = csv.writer(ofile, lineterminator="\n")
			table = BeautifulSoup(html, "html5lib")
			header = table.find("div", {"class": "k-grid-header"})
			attributes = header.findAll("th")
			head = []

			for attr in attributes:
				a = attr.get("data-field")

				if a:
					head.append(a)

			if p != 7:
				# Table is set up funny for all positions except for defenses.
				# Move the 4th and 5th val to the end
				head.append(head.pop(6))
				head.append(head.pop(6))

			head.insert(4, "Season")

			csv_ofile.writerow(head)
			idents = table.find("div", {"class": "k-grid-content-locked"})
			idents_rows = idents.findAll("tr")
			stats = table.find("div", {"class": "k-grid-content k-auto-scrollable"})
			stats_rows = stats.findAll("tr")

			for ident, stat in zip(idents_rows, stats_rows):
				record = []
				i = ident.findAll("td")

				for x in i:
					record.append(re.sub(r"\s+", "", x.text))

				st = stat.findAll("td")

				for y in st:
					record.append(re.sub(r"\s+", "", y.text))

				record.insert(4, s)
				csv_ofile.writerow(record)
