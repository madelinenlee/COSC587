#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 12:34:09 2018

@author: madeline
"""

#check redundant data
    #percentage of redundant data 
#how to check for noise?
    #negative values, not in team list, 
#position data (how to separate, if to)
    #keep in list in data frame
#do teams match up
#missing values (N/A)

#fantasy prediction
    
#fill null with zeroes
#run again


import numpy as np
import pandas as pd
from pprint import pprint
import csv

if __name__ == '__main__':

    #read in data
    historical_data = pd.read_csv('pro-football-reference.csv', sep=',', encoding='latin1')

    
    #function to count the number of null values per attribute, store in dict
    def fraction_missing_hist_score(data_frame):
        #print('find fraction of missing values per attribute')
        fraction_missing = {} #create empty dictionary
        attributes = data_frame.columns.tolist() #get list of attributes
        for item in attributes: #loop through attributes
            missing_data = data_frame[data_frame[item].isnull() == True] #determine where null values
            fraction_missing[item] = missing_data.shape[0]/data_frame.shape[0] #calculate fraction, add to dict
        return(fraction_missing)

    #get number of invalid/noisy values per attribute
    def noise_data_hist_score(data_frame):
        #print('find fraction of invalid values per attribute')
        object_invalid = {} #create empty dictionary

        opp_invalid = data_frame[data_frame['opp'].str.len() != 3] #determine rows where opp name is invalid
        object_invalid['opp'] = opp_invalid.shape[0] #add to dictionary
        team_invalid = data_frame[data_frame['team'].str.len() != 3] #determine rows where team name is invalid
        object_invalid['team'] = team_invalid.shape[0] #add to dictionary
        
        #position data was removed from calculating the cleaning score because it became
        #apparent that players could have more than one position. since there is no
        #limit to the number of positions a player could hold, we removed this check
        #from the score after analyzing the data.
        
        #position_invalid = data_frame[data_frame['position'].str.len() > 2]
        #object_invalid['position'] = position_invalid.shape[0]
        
        
        date_invalid = data_frame[data_frame['game_date'].str.len() > 10 ] #determine rows where date is invalid format
        object_invalid['game_date'] = date_invalid.shape[0] #add to dictionary
        
        for item in object_invalid:
            object_invalid[item] = object_invalid[item]/data_frame.shape[0] #determine fraction invalid data per attribute
            
        return(object_invalid)

    #check that all teams are represented, played against (if they dont match
    #then an error in the set of teams exists)      
    def hist_team_opp_match(data_frame):
        #print('determine if teams and opponents lists match')
        team_list = data_frame['team'].unique()
        team_list.sort()
        opp_list = data_frame['opp'].unique()
        opp_list.sort()
        if np.array_equal(team_list, opp_list):
            return  (0) #lower scores are the goal, so return 0 instead of 1
        else:
            return(1)
    
    #get fraction of duplicate rows per dataset
    def duplicates_hist_score(data_frame):
        #print('find fraction of duplicate rows in dataset')
        
        #must temporarily drop position from dataframe in order to determine if duplicate rows
        #since position is a list object
        
        drop_position = data_frame.drop(['position'], axis=1)
        duplicate_data = drop_position[drop_position.duplicated() == True] #find rows of duplicate data
        return(duplicate_data.shape[0]/data_frame.shape[0]) #get fraction of duplicate data in dataset

    
    #remove non numeric attributes from attribute list, then determine
    #how many negative values exist per attribute that should not have neg values
    def non_negative_hist_score(data_frame):
        #print('find number of negative values per proper numeric attribute')
        
        #list of object attributes, attributes where negative values are OK, determined by experts (us)
        non_pos = ['team','opp','player','game_date','position','catch_pct',\
                   'rush_yds','rush_yds_per_att','pass_yds','pass_yds_per_att',\
                   'pass_adj_yds_per_att','kick_ret_yds','kick_ret_yds_per_ret',\
                   'punt_ret_yds','punt_ret_yds_per_ret']
        
        pos_numeric_attributes = data_frame.columns.tolist()
        
        #remove these from attribute list so that a loop can be written to
        #quickly ascertain if negative values exist in non-neg attributes
        for item in non_pos:
            pos_numeric_attributes.remove(item)
    
        #find fraction of invalid/noisy values per numeric attribute
        numeric_invalids = {}
        for item in pos_numeric_attributes:
            negative_data = data_frame[data_frame[item] < 0 ]
            numeric_invalids[item] = negative_data.shape[0]/data_frame.shape[0]
        return(numeric_invalids)

    #generate final cleaning score
    #lower score is better
    def clean_hist_score(data_frame):
        fraction_missing = fraction_missing_hist_score(data_frame)
        duplicate = 0
        duplicates_hist_score(data_frame)
        noise_data = noise_data_hist_score(data_frame)
        non_neg = non_negative_hist_score(data_frame)
        clean_list = [fraction_missing, noise_data, non_neg]
        count = 0
        clean_score = 0
        
        #add up all fractions while keeping list of total # attributes
        for score in clean_list:
            for item in score:
                count = count+1
                clean_score = clean_score + score[item]
            #print(count)
            
        #add boolean matching score and fraction of dupliate rows       
        clean_score = clean_score + hist_team_opp_match(data_frame) + duplicate
        
        #increase count to reflect the highest possible score 
        count = count + 2
        
        #calculate percentage of cleanliness
        clean_percent_score = clean_score/count
            
        print('cleaning score out of ' + str(count) + ': ' + str(clean_score))
        print('percentage: ' + str(clean_percent_score))
        print('note: a lower percentage is better')
        return (clean_percent_score)

    clean_hist_score(historical_data)
