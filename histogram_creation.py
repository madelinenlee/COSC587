#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 20:29:55 2018

@author: madeline
"""

import pandas as pd
import numpy as np
import pprint
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt

#load datasets in
predicted_data = pd.read_csv('clean_fantasy_data.csv' , sep=',')
merged_data = pd.read_csv('merged_data.csv', sep=',')

#function creates boxplot of one attribute, grouped by another attribute
#takes in pandas dataframe, string, string
def create_boxplot(data_frame, attribute, group_by):
    if group_by == '' or group_by.lower() == 'none':
        plt.style.use = 'default'
        data_frame.boxplot(column = attribute)
        plt.title("Box plots of " + "attribute" + " in " + str(data_frame) + " data set")
        plt.savefig(attribute + 'box_plot.png') #saves figure in same directory
    else:
        plt.style.use = 'default'
        data_frame.boxplot(column = attribute, by=group_by)
        plt.title("Box plots of " + "attribute" + " in " + str(data_frame) + " data set")
        plt.savefig(attribute + 'box_plot.png')#saves figure in same directory 
        
#create_boxplot(merged_data, 'rec_yds', 'position')

#function creates histogram of one attribute, grouped by another attribute
#takes in pandas dataframe, string, string
def create_hist(data_frame, attribute, group_by):
    if group_by == '' or group_by.lower() == 'none':
        plt.title(attribute)
        data_frame[attribute].hist()
        plt.savefig(attribute)
    else:
        group_by_list = data_frame[group_by].unique().tolist()
        for item in group_by_list:
            p_data = data_frame[data_frame[group_by] == item]
            p_data[attribute].hist()
            plt.title( item + ", Age")
            plt.show()
            
#create_hist(merged_data, 'rec_yds', '')
#create_hist(merged_data, 'rec_yds', 'position')

#function creates scatterplot of two attributes, grouped by another attribute
#takes in pandas dataframe, string, string, string 
def create_scatterplot(data_frame, x, y, group_by):
    if group_by == '' or group_by.lower() == 'none':
        temp_plot = data_frame.plot.scatter(x = x, y = y)
        plt.title(x + ' vs. ' + y )
        plt.show()
    else:
        group_by_list = data_frame[group_by].unique().tolist()
        for item in group_by_list:
            p_data = data_frame[data_frame[group_by] == item]
            temp_plot = p_data.plot.scatter(x = x, y = y)
            plt.title(item + ', ' + x + ' vs. ' + y)
    return temp_plot

#create_scatterplot(predicted_data, 'RushingYards', 'FantasyPointsPerGame', 'Position')

#function calculates correlation of two attribute, grouped by another attribute
#takes in pandas dataframe, string, string, string
def correlation(data_frame, x, y, group_by):
    print('correlation coefficient between ' + x + ' and ' + y)
    if group_by == 'none' or group_by == '':
        print(data_frame[x].corr(data_frame[y]))
    else:
        group_by_list = data_frame[group_by].unique().tolist()
        for item in group_by_list:
            temp_data_frame = data_frame[data_frame[group_by] == item]
            print(item + ': ')
            print(temp_data_frame[x].corr(temp_data_frame[y]))

#correlation(merged_data, 'age', 'rec_yds', 'none')
