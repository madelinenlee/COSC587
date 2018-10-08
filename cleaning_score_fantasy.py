#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 15:07:59 2018

@author: madeline
"""

import numpy as np
import pandas as pd

if __name__ == '__main___':
    
    fantasy_data = pd.read_csv('fantasy-data.csv', sep=',', encoding='latin1')
    
    def fraction_missing_fan_score(data_frame):
            fraction_missing = {}
            attributes = data_frame.columns.tolist()
            for item in attributes:
                missing_data = data_frame[data_frame[item].isnull() == True]
                fraction_missing[item] = missing_data.shape[0]/data_frame.shape[0]
            return(fraction_missing)
    
    #get number of invalid/noisy values per attribute
    def noise_data_fan_score(data_frame):
        object_invalid = {}
    
        opp_invalid = data_frame[data_frame['Opponent'].str.len() > 3]
        object_invalid['Opponent'] = opp_invalid.shape[0]
        team_invalid = data_frame[data_frame['Team'].str.len() > 3]
        object_invalid['Team'] = team_invalid.shape[0]
        position_invalid = data_frame[data_frame['Position'].str.len() > 2]
        object_invalid['Position'] = position_invalid.shape[0]
        #date_invalid = data_frame[data_frame['game_date'].str.len() > 10 ]
        #object_invalid['game_date'] = date_invalid.shape[0]
        
        for item in object_invalid:
            object_invalid[item] = object_invalid[item]/data_frame.shape[0]
            
        return(object_invalid)
            
    def team_opp_fan_match(data_frame):
            team_list = data_frame['Team'].unique()
            team_list.sort()
            opp_list = data_frame['Opponent'].unique()
            opp_list.sort()
            if np.array_equal(team_list, opp_list):
                return  (0)
            else:
                return(1)
        
    #get fraction of duplicate rows per dataset
    def duplicates_fan_score(data_frame):
        duplicate_data = data_frame[data_frame.duplicated() == True]
        #data_frame.drop_duplicates()
        return(duplicate_data.shape[0]/data_frame.shape[0])
    
    
    #remove non numeric attributes from attribute list, then determine
    #how many negative values exist per attribute that should not have neg values
    def non_negative_fan_score(data_frame):
        #list of object attributes, attributes where negative values are OK
        non_pos = ['Team','Opponent','Name','Position','RushingYards',\
                   'PassingYards','PassingYardsPerAttempt','RushingYardsPerAttempt']
      
        pos_numeric_attributes = data_frame.columns.tolist()
        #remove these from attribute list so that a loop can be written to
        #quickly ascertain if negative values exist in non-neg attributes
        for item in non_pos:
            pos_numeric_attributes.remove(item)
    
        #find fraction of invalid/noisy values per numeric attribute
        numeric_invalids = {}
        for item in pos_numeric_attributes:
            negative_data = data_frame[data_frame['RushingAttempts'] < 0 ]
            numeric_invalids[item] = negative_data.shape[0]/data_frame.shape[0]
        return(numeric_invalids)
    
    #non_negative_score(fantasy_data)
    
    #generate final cleaning score, a lower score is better
    def clean_fan_score(data_frame):
        fraction_missing = fraction_missing_fan_score(data_frame)
        duplicate = duplicates_fan_score(data_frame)
        noise_data = noise_data_fan_score(data_frame)
        non_neg = non_negative_fan_score(data_frame)
        clean_list = [fraction_missing, noise_data, non_neg]
        count = 0
        clean_score = 0
        #add up all fractions while keeping list of total # attributes
        for score in clean_list:
            for item in score:
                count = count+1
                clean_score = clean_score + score[item]
            
        #add boolean matching score and fraction of dupliate rows       
        clean_score = clean_score + team_opp_fan_match(data_frame) + duplicate
        
        #increase count to reflect the highest possible score 
        count = count + 2
    
        #get percentage of cleanliness    
        clean_percent_score = clean_score/count
            
        print('cleaning score out of ' + str(count) + ': ' + str(clean_score))
        print('percentage: ' + str(clean_percent_score))
        print('note: a lower percentage is better')
    
    #test
    #clean_fan_score(fantasy_data)
