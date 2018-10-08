#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 20:09:33 2018

@author: madeline
"""

import numpy as np
import pandas as pd
from pprint import pprint
import csv
import cleaning_score_fantasy as csf


#read data in
if __name__ == '__main___':

    fantasy_data = pd.read_csv('fantasy-data.csv', sep=',', encoding='latin1')
    
    #replace all NAN values (numerical) with true zeroes, since these values
    #are true zeroes
    def clean_int_fan_null(data_frame):
        numeric_attributes = data_frame.columns.tolist()
        non_numeric_list = data_frame.select_dtypes(include=['object']).columns.tolist()
        for item in non_numeric_list:
            numeric_attributes.remove(item)
            
        for item in numeric_attributes:
                data_frame[item].fillna(0, inplace = True)
        return(data_frame)
    
    #remove rows with defensive data aka DST because we are only predicting offensive data    
    def clean_fan_position(data_frame):
        offense_data_frame = data_frame[data_frame['Position'].str.len() <= 2]
        return(offense_data_frame)
    
    #remove duplicate rows 
    def drop_fan_duplicates(data_frame):
        data_frame.drop_duplicates()
        return(data_frame)
    
    #run cleaning score again, write clean dataset to csv 
    def fantasy_clean_process(data_frame):
        #run all cleaning functions
        print('running cleaning score...')
        csf.clean_fan_score(data_frame)
        
        print('cleaning ....')
        #drop duplicates
        no_dup = drop_fan_duplicates(data_frame)
        
        #drop defensive positions
        no_def = clean_fan_position(no_dup)
        
        #fill nAns with true zeroes
        final_clean = clean_int_fan_null(no_def)
        
        print('re-running cleaning score... ')
        csf.clean_fan_score(final_clean)
        
        final_clean.to_csv('clean_fantasy_data.csv', sep=',')
        
        #return(final_clean)
        
    #run total process 
    fantasy_clean_process(fantasy_data)