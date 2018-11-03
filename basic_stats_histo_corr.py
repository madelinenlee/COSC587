#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 19:44:15 2018
@author: madeline
"""
# libraries
import pandas as pd
import numpy as np
import pprint
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
import math

# load data in, must be in same directory

weather_data = pd.read_csv('weather_cleaned.csv', sep=',')
predicted_data = pd.read_csv('clean_fantasy_data.csv', sep=',')
merged_data = pd.read_csv('merged_data.csv', sep=',')


# -----------------------------Basic Attributes ------------------------


# get basic statistics of 10 attributes

# merged_data['kickoff_barometer_x'].describe()
# merged_data['kickoff_humidity_x'].describe()
# predicted_data['FantasyPointsPerGame'].describe()
# merged_data['age'].describe()
# merged_data['rush_yds'].describe()
# merged_data['rec_yds'].describe()
# predicted_data['ReceivingYards'].describe()
# merged_data['pass_yds'].describe()
# merged_data['pass_td'].describe()
# merged_data['rec'].describe()

def describe_by(data_frame, attribute, group_by):
    print('describe ' + attribute + ' by ' + group_by)
    group_by_list = data_frame[group_by].unique().tolist()
    for item in group_by_list:
        print(item)
        temp_data_frame = data_frame[data_frame[group_by] == item]
        print(temp_data_frame[attribute].describe())


# testing
# describe_by(merged_data, 'pass_yds', 'position')

# how to find outliers
# look at min-max of descriptive statistics (ie fantasy points per game, age)
# make box plots of each variable (?)

# ---------------------find outliers in each attribute-------------------------

def create_boxplot(data_frame, attribute, group_by):
    if group_by == '' or group_by.lower() == 'none':
        plt.style.use = 'default'
        data_frame.boxplot(column=attribute)
        plt.title("Box plots of " + "attribute" + " in " + str(data_frame) + " data set")
        plt.savefig(attribute + 'box_plot.png')
    else:
        plt.style.use = 'default'
        data_frame.boxplot(column=attribute, by=group_by)
        plt.title("Box plots of " + "attribute" + " in " + str(data_frame) + " data set")
        plt.savefig(attribute + 'box_plot.png')


# testing
# create_boxplot(merged_data, 'rec_yds', 'position')

# -------------------------------binning-------------------------------
# for one numeric attribute, write code to bin
# bin age
minAge = merged_data["age"].min()
maxAge = merged_data["age"].max()
minAge = minAge - 1
maxAge = maxAge + 1
print("age range: ", minAge, maxAge)

# Create even spaced bins using min and max
names = range(1, 7)
bins = np.arange(minAge, maxAge, 4)
bins = bins.tolist()
for i in range(0, len(bins)):
    bins[i] = math.floor(bins[i])

merged_data['bin1_age'] = pd.cut(merged_data['age'], bins, labels=names)

# second binning strategy - equidepth
names = range(1, 6)

bins2 = [0, 20, 24, 26, 28, 45]
merged_data['bin2_age'] = pd.cut(merged_data['age'], bins2, labels=names)

# third binning strategy: equal

# histograms for binning to analyze best binning strategy
# create_hist(merged_data, 'bin1_age', '')
# create_hist(merged_data, 'bin2_age', '')


# -------------------histogram for 6 variables------------------------

# create 3 histograms of attributes

plt.title("Kickoff Humidity")
merged_data.hist('kickoff_humidity_x')
# plt.show()
plt.savefig('kickoff_humidity_histogram.png')

plt.title("Kickoff Barometer")
merged_data.hist('kickoff_barometer_x')
# plt.show()
plt.savefig('kickoff_barometer_histogram.png')

# Basic plotting - histogram of Age values
merged_data['age'].hist()
plt.title("Age")
# plt.show()
plt.savefig('age_distribution.png')

# create histograms for age, grouped by position
for item in position_list:
    p_data = merged_data[merged_data['position'] == item]
    p_data['age'].hist()
    plt.title(item + ", Age")
    plt.show()

# create histogram for fantasy points per game
plt.title('Fantasy Points Per Game')
predicted_data.hist('FantasyPointsPerGame')
plt.savefig('fantasy_points_histogram.png')

# create histogram for receiving yards, grouped by position
merged_data['rec_yds'].hist(by=merged_data['position'])
plt.title('Receiving Yards')
plt.savefig('receiving_yards_histogram.png')


# function for creating histogram
# input: data frame, attribute to make histogram, attribute to group by
def create_hist(data_frame, attribute, group_by):
    if group_by == '':
        plt.title(attribute)
        data_frame[attribute].hist()
        plt.savefig(attribute + '_histogram.png')
    else:

        data_frame[attribute].hist(by=data_frame[group_by])
        plt.title(attribute)
        plt.savefig(attribute + '_' + group_by + '_histogram.png')


# create_hist(merged_data, 'age', '')
# create_hist(merged_data, 'kickoff_barometer_x', '')
# create_hist(merged_data, 'kickoff_barometer_x', '')

# create_hist(predicted_data, 'FantasyPointsPerGame', 'Position')

# -----------------------------analysis-------------------------------

# 3 quant variables, show correlation between all pairs
# age, rec_yds, humidity, rush_yds

# definition to create scatterplot of 2 attributes
# input: data frame, attribute1, attribute 2, attribute to group by
def create_scatterplot(data_frame, x, y, group_by):
    if group_by == '':
        temp_plot = data_frame.plot.scatter(x=x, y=y)
        plt.title(x + ' vs. ' + y)
        plt.savefig(x + '_vs_' + y + '.png')

    else:
        group_by_list = data_frame[group_by].unique().tolist()
        for item in group_by_list:
            p_data = data_frame[data_frame[group_by] == item]
            temp_plot = p_data.plot.scatter(x=x, y=y)
            plt.title(item + ', ' + x + ' vs. ' + y)
            plt.savefig(item + '_' + x + '_vs._' + y + '.png')

    return temp_plot


# create scatterplots of attributes

# create_scatterplot(merged_data, 'age', 'rec_yds', 'position')
# create_scatterplot(merged_data, 'age', 'rush_yds', '')
# create_scatterplot(merged_data, 'age', 'kickoff_humidity_x', '')
# create_scatterplot(merged_data, 'rec_yds', 'rush_yds',  '')
# create_scatterplot(merged_data, 'rec_yds', 'age',  '')
# create_scatterplot(merged_data, 'rec_yds', 'kickoff_humidity_x',  '')
# create_scatterplot(merged_data, 'kickoff_humidity_x', 'age',  '')
# create_scatterplot(merged_data, 'kickoff_humidity_x', 'rush_yds',  '')
# create_scatterplot(merged_data, 'kickoff_humidity_x', 'rec_yds',  '')
# create_scatterplot(merged_data, 'rush_yds', 'age',  '')
# create_scatterplot(merged_data, 'rush_yds', 'rec_yds', '')
# create_scatterplot(merged_data, 'rush_yds', 'age', '')

# scatterplots grouped by position

# example:
# create_scatterplot(merged_data, 'age', 'rec_yds', 'position')


# ------------get correlation coefficient between two variables------------

# definition to get correlation between two attributes
# input: data frame, attribute 1, attribute 2, which variable to group by
def correlation(data_frame, x, y, group_by):
    print('correlation coefficient between ' + x + ' and ' + y)
    if group_by == '':
        print(data_frame[x].corr(data_frame[y]))
    else:
        group_by_list = data_frame[group_by].unique().tolist()
        for item in group_by_list:
            temp_data_frame = data_frame[data_frame[group_by] == item]
            print(item + ': ')
            print(temp_data_frame[x].corr(temp_data_frame[y]))

# run correlations on each of the variables
# correlation(merged_data, 'age', 'rec_yds', 'position')
# correlation(merged_data, 'age', 'rush_yds', '')
# correlation(merged_data, 'age', 'kickoff_humidity_x', '')
# correlation(merged_data, 'rec_yds', 'rush_yds',  '')
# correlation(merged_data, 'rec_yds', 'age',  '')
# correlation(merged_data, 'rec_yds', 'kickoff_humidity_x',  '')
# correlation(merged_data, 'kickoff_humidity_x', 'age',  '')
# correlation(merged_data, 'kickoff_humidity_x', 'rush_yds',  '')
# correlation(merged_data, 'kickoff_humidity_x', 'rec_yds',  '')
# correlation(merged_data, 'rush_yds', 'age',  '')
# correlation(merged_data, 'rush_yds', 'rec_yds', '')
# correlation(merged_data, 'rush_yds', 'age', '')