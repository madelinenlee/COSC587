#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 12:13:53 2018

@author: madeline
"""

import numpy as np
import pandas as pd
from pprint import pprint
import csv
import cleaning_score_historical

if __name__ == '__main__':

        #read in data
    historical_data = pd.read_csv('pro-football-reference.csv', sep=',', encoding='latin1')
    
    #clean_score(historical_data)
    
    #function to get rid of duplicate rows
    def clean_hist_duplicates(data_frame):
        data_frame.drop_duplicates()
        return(data_frame)
        
    #function to reassign position to list object  because players can have more 
    #than one position
    def clean_hist_position(data_frame):
        for i in range(data_frame.shape[0]):
            if '-' in data_frame.loc[i, 'position']:
                data_frame.at[i, 'position'] = data_frame.loc[i, 'position'].split('-')
                #print(data_frame.loc[i, 'position'])
            elif ',' in data_frame.loc[i, 'position']:
                data_frame.at[i, 'position'] = data_frame.loc[i, 'position'].split(',')
                #print(data_frame.loc[i, 'position'])
        return(data_frame)
    
    #after examining position unique data, realize that players can have multiple
    #positions, convert positions column to list object instead of string.
    #realize this changes the way cleaning score should be measured for position
    #omit position from being checked in noisy data - as long as not null,
    #position data is OK
    
    #convert catch percentage attribute from string to float
    #can't get this to work :/ 
    '''def clean_catch_pct(data_frame):
        percent_data = my_data['catch_pct'].replace(r'%',r'0').astype(float)/100.0
        for i in range(63371, data_frame.shape[0]):
            if '%' in data_frame.at[i, 'catch_pct']:
                strip_percent = str(data_frame.loc[i, 'catch_pct']).strip('%')
            data_frame.at[i, 'catch_pct'] = str(float(strip_percent)/100)'''


    #replace all numeric attributes with null values to zero
    def clean_hist_int_nulls(data_frame):
        numeric_attributes = data_frame.columns.tolist() #get list of all attributes
        
        #get list of object attributes 
        non_numeric_list = data_frame.select_dtypes(include=['object']).columns.tolist()
        
        #remove object attributes from numeric attributes list
        for item in non_numeric_list:
            numeric_attributes.remove(item)
        
        #replace nANs with true zeroes, as determiend by project leaders
        for item in numeric_attributes:
            data_frame[item].fillna(0, inplace = True)
            
        return(data_frame)
        
    #run cleaning process
    def hist_clean_process(data_frame): 
        print('running initial cleaning score...')
        clean_hist_score(data_frame)
        
        print('cleaning ....')
        
        
        #remove duplicates
        no_dup = clean_hist_duplicates(data_frame)
        #assign null values
        no_null = clean_hist_int_nulls(no_dup)
        
        #put position from string to list format
        final_data = clean_hist_position(no_null)
                
        print('re-running cleaning score... ')
        clean_hist_score(final_data)
        
        return(final_data)
    

    hist_clean_process(historical_data)
    
    