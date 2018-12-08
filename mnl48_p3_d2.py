#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 10:20:25 2018

@author: madeline
"""

import pandas as pd
import numpy as np
import plotly
plotly.tools.set_credentials_file(username='madelinelee', api_key='FW2B67yKVADiMx2Ahz5G')

import plotly.plotly as py
from plotly import tools
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
from scipy import stats

from statistics import mean

merged_data = pd.read_csv('merged_data.csv')

#function to create boxplots of average humidity from 2013-2017 by team
def create_humidity_box_by_team():
    data_list = []
    #get list of teams
    team_list = merged_data['team'].unique().tolist()
    #create subsets and calculate average year humidity, add to list, create boxplot
    #append boxplot to data list
    for item in team_list:
        y1 = []
        team_subset = merged_data[merged_data['team'] == item]
        year_list = team_subset['year_id'].unique().tolist()
        for year in year_list:
            year_team_data = team_subset[team_subset['year_id'] == year]
            game_date_data = year_team_data.drop_duplicates('game_date', inplace = False)
            #print(game_date_data)
            year_humidity = game_date_data['kickoff_humidity_x'].tolist()
            #print(year_humidity)
            avg_year_humidity = mean(year_humidity)
            #print(avg_year_humidity)
            y1.append(avg_year_humidity)
            
        trace = go.Box(
                y=y1,
                name = item,
                )
            
        data_list.append(trace)
    layout = go.Layout(
            title = "Average Yearly Humidity Per Team"
            )
    fig = go.Figure(data=data_list,layout=layout)
    
    py.iplot(fig, filename = 'Average Yearly Humidity Per Team')
 
    #function to create set of subplots that measure pass yards and rush yards vs visibility
def create_visibility_pass_yds_rush_yds():
    qb_data = merged_data[merged_data['position'] == 'QB']
    rb_data = merged_data[merged_data['position'] == 'RB']
    qb_trace = go.Scatter(
            x = qb_data['kickoff_visibility_x'].tolist(),
            y = qb_data['pass_yds'].tolist(),
            mode = 'markers'
            )
    rb_trace = go.Scatter(
            x = rb_data['kickoff_visibility_x'].tolist(),
            y = rb_data['rush_yds'].tolist(),
            mode = 'markers'
            )
    
    fig = tools.make_subplots(rows=1, cols=2)

    fig.append_trace(qb_trace, 1, 1)
    fig.append_trace(rb_trace, 1, 2)
    
    fig['layout']['xaxis1'].update(title='kickoff visibility', range=[0,65])
    fig['layout']['xaxis2'].update(title='kickoff visibility', range=[0,65])
    
    fig['layout']['yaxis1'].update(title='pass yards', range=[0, 600])
    fig['layout']['yaxis2'].update(title='rushing yards', range=[0, 600])
    
    fig['layout'].update(height=700, width=1000, title='qb vs rb visibility')
    py.iplot(fig, filename='qb_vs_rb_visibility')


#function to create subplot of qb vs wr humidity,
#pass yards and receiving yards vs humidity
def create_humidity_wr_graphs():
    #data_list = []
    wr_data = merged_data[merged_data['position'] == 'WR']
    qb_data = merged_data[merged_data['position'] == 'QB']
    
    wr_trace = go.Scatter(
            x = wr_data['kickoff_humidity_x'].tolist(),
            y = wr_data['rec_yds'].tolist(),
            mode = 'markers'
            )
    qb_trace = go.Scatter(
            x = qb_data['kickoff_humidity_x'].tolist(),
            y = qb_data['pass_yds'].tolist(),
            mode = 'markers'
            )
    fig = tools.make_subplots(rows=1, cols=2)

    fig.append_trace(qb_trace, 1, 1)
    fig.append_trace(wr_trace, 1, 2)
    
    fig['layout']['xaxis1'].update(title='kickoff humidity', range=[0,100])
    fig['layout']['xaxis2'].update(title='kickoff humidity', range=[0,100])
    
    fig['layout']['yaxis1'].update(title='pass yards', range=[0, 600])
    fig['layout']['yaxis2'].update(title='receiving yards', range=[0, 600])
    
    fig['layout'].update(height=600, width=800, title='qb vs wr humidity')
    py.iplot(fig, filename='qb_vs_wr_humidity')
    
    
#layered plot with home vs away scoring, function requires team input
def graph_scoring_home_away_by_team(team):
    scoring_team_data = merged_data[merged_data['team'] == team]
    home_data = scoring_team_data[scoring_team_data['away'] == 0]
    away_data = scoring_team_data[scoring_team_data['away'] == 1]
    
    home_date_data = home_data['game_date'].unique().tolist()

    away_date_data = away_data['game_date'].unique().tolist()
    
    #print(away_date_data)
    
    home_scoring_y = []
    for date in home_date_data:
        date_subset = home_data[home_data['game_date'] == date]
        #print(date_subset)
        scoring_list = date_subset['scoring'].tolist()
        total = sum(scoring_list)
        home_scoring_y.append(total)


    away_scoring_y = []
    for date in away_date_data:
        date_subset = away_data[away_data['game_date'] == date]
        scoring_list = date_subset['scoring'].tolist()
        total = sum(scoring_list)
        away_scoring_y.append(total)
    
    scoring_team_data['game_date'] = pd.to_datetime(scoring_team_data['game_date'])
    scoring_team_data = scoring_team_data.drop_duplicates('game_date', inplace = False)
    x_list = scoring_team_data['game_date'].tolist()
    x_list.sort()
    
    home_data['game_date'] = pd.to_datetime(home_data['game_date'])
    home_data = home_data.drop_duplicates('game_date', inplace = False)
    away_data['game_date'] = pd.to_datetime(away_data['game_date'])
    away_data = away_data.drop_duplicates('game_date', inplace = False)
    
    home_data_x = home_data['game_date'].tolist()
    home_data_x.sort()
    
    away_data_x = away_data['game_date'].tolist()
    away_data_x.sort()
    
    home_scoring = go.Scatter(x=home_data_x,
                              y=home_scoring_y,
                              name='Home Scoring',
                              line=dict(color='#33CFA5'))
    away_scoring = go.Scatter(x=away_data_x,
                              y=away_scoring_y,
                              name='Away Scoring',
                              line=dict(color='#F06A6A', dash='dash')
                                        )

    data = [home_scoring, away_scoring]

    updatemenus = list([
    dict(type="buttons",
         active=-1,
         buttons=list([
            dict(label = 'Home Scoring',
                 method = 'update',
                 args = [{'visible': [True, False]},
                         {'title': 'Home Scoring vs Date',
                          'annotations': []}]
                         ),
            dict(label = 'Away Scoring',
                 method = 'update',
                 args = [{'visible': [False,True]},
                         {'title': 'Away Scoring vs Date',
                          'annotations': []}]),
            dict(label = 'Both',
                 method = 'update',
                 args = [{'visible': [True, True]},
                         {'title': team + 'Scoring vs Date',
                          'annotations': []}]),
            dict(label = 'Reset',
                 method = 'update',
                 args = [{'visible': [True, True]},
                         {'title': team + 'Scoring vs Date',
                          'annotations': []}])
            ]),
        )
    ])
    
    layout = dict(title=team + ' Scoring',
                  showlegend=False,
                  xaxis = dict( title = 'Date'),
              updatemenus=updatemenus)

    fig = dict(data=data, layout=layout)
    py.iplot(fig, filename=team+'_scoring')

#graph_scoring_home_away_by_team('PIT')
#graph_scoring_home_away_by_team('ARI')
#graph_scoring_home_away_by_team('KAN')
#graph_scoring_home_away_by_team('MIA')
#graph_scoring_home_away_by_team('SEA')


#create graph to make time series of weather attributes:
    #humidity, visibility, pressure measured over time 
def graph_weather_attributes(team):
    team_data = merged_data[merged_data['team'] == team]
    team_data = team_data.drop_duplicates('game_date', inplace = False)
    team_data = team_data[team_data['away'] == 0]
    #team_data.sort_values(by='game_date')
    #print(team_data['game_date'].tolist())
    team_data['game_date'] = pd.to_datetime(team_data['game_date'])
    team_data.sort_values(by='game_date', ascending=True)
    x_list = team_data['game_date'].tolist()
    x_list.sort()
    #print(x_list)
    #print(team_data['game_date'].tolist())
    #print(team_data['kickoff_humidity_x'].tolist())

    
    humidity = go.Scatter(x=x_list,
                              y=team_data['kickoff_humidity_x'].tolist(),
                              name= 'Humidity (%)',
                              line=dict(color='#33CFA5')
                                        )
                                        
    visibility = go.Scatter(x=x_list,
                              y=team_data['kickoff_visibility_x'].tolist(),
                              name= 'Visibility (mi)',
                              line=dict(color='#F06A6A', dash='dash')
                                        )
    barometer = go.Scatter(x = x_list,
                           y = team_data['kickoff_barometer_x'].tolist(),
                           name = 'Barometer (in)',
                           line = dict(color='blue', dash='dot')
                           )
    
    data = [humidity, visibility, barometer]
    
    updatemenus = list([
    dict(type="buttons",
         active=-1,
         buttons=list([
            dict(label = 'Humidity',
                 method = 'update',
                 args = [{'visible': [True, False, False]},
                         {'title': team + ' Humidity (%) vs Date',
                          'annotations': []}]
                         ),
            dict(label = 'Visibility',
                 method = 'update',
                 args = [{'visible': [False,True, False]},
                         {'title': team + ' Visibility (mi)vs Date',
                          'annotations': []}]),
            dict(label = 'Pressure',
                 method = 'update',
                 args = [{'visible': [False,False, True]},
                         {'title': team + ' Barometer (in) vs Date',
                          'annotations': []}]),    
            dict(label = 'All',
                 method = 'update',
                 args = [{'visible': [True, True, True]},
                         {'title': team + 'Weather Metrics vs Date',
                          'annotations': []}]),
            dict(label = 'Reset',
                 method = 'update',
                 args = [{'visible': [True, True, True]},
                         {'title': team + 'Weather Metrics vs Date',
                          'annotations': []}])
            ]),
        )
    ])
     
    layout = dict(title=team + ' Weather Metrics vs Date', showlegend=False,
                  xaxis=dict(
                        title = 'Date'
                        ),
                  yaxis=dict(
                        title = 'Humidity (%), Visibility(mi), Barometer(in)'
                        ),
                updatemenus=updatemenus)

    fig = dict(data=data, layout=layout)
    py.iplot(fig, filename= team + '_weather_metrics')

#graph_weather_attributes('PIT')
#graph_weather_attributes('ARI')
#graph_weather_attributes('MIA')
#graph_weather_attributes('SEA')
#graph_weather_attributes('KAN')


#create graph to determine how wind speed affects
    #pass yards, field goal percentage, rush yards
def wind_spd_vs_other():
    drop_null_wind = merged_data.dropna(subset=['kickoff_wind_x'])
    drop_null_wind["wind_intensity"], drop_null_wind["wind_direction"] = zip(*drop_null_wind['kickoff_wind_x'].apply(lambda x: x.split("mi")))
    
    wind_speed_list = drop_null_wind['wind_intensity'].unique().tolist()
    for i in range(0, len(wind_speed_list)):
        wind_speed_list[i] = int(wind_speed_list[i])
    wind_speed_list.sort()

    #print(wind_speed_list)
    pass_yds = []
    rec_yds = []
    fgp = []
    rush_yds = []
    for speed in wind_speed_list:
        wind_subset = drop_null_wind[drop_null_wind['wind_intensity'] == str(speed)]
        
        qb_data = wind_subset[wind_subset['position'] == 'QB']
        pass_yd_temp_avg = mean(qb_data['pass_yds'].tolist())
        pass_yds.append(pass_yd_temp_avg)

        wr_data = wind_subset[wind_subset['position'] == 'WR']
        rec_yd_temp_avg = mean(wr_data['rec_yds'].tolist())
        rec_yds.append(rec_yd_temp_avg)    
        
        k_data = wind_subset[wind_subset['position'] == 'K']
        fgp_temp_avg = mean(k_data['fg_perc'].tolist())
        fgp.append(fgp_temp_avg)
        
        rb_data =wind_subset[wind_subset['position'] == 'RB']
        rush_yd_temp_avg = mean(rb_data['rush_yds'].tolist())
        rush_yds.append(rush_yd_temp_avg)
    
    #print('passyds')
    #print(pass_yds)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(wind_speed_list,rec_yds)
    
    wr_line = slope*wind_speed_list+intercept
        
    qb = go.Scatter(x=wind_speed_list,
                              y=pass_yds,
                              name= 'QB Pass Yds',
                              line=dict(color='#33CFA5')
                                        )
                              
    wr = go.Scatter(x=wind_speed_list,
                              y=rec_yds,
                              name= 'WR Receiving Yds',
                              line=dict(color='orange')
                                        )
    
    k = go.Scatter(x=wind_speed_list,
                              y=fgp,
                              name= 'K Field Goal Percentage',
                              line=dict(color='blue')
                                        )
                              
    rb = go.Scatter(x=wind_speed_list,
                              y=rush_yds,
                              name= 'RB Rushing Yds)',
                              line=dict(color='#F06A6A')
                                        )
    
    data = [qb, wr, k, rb, wr_line]
    
    #drop_null_wind['wind_intensity'].tolist()
    updatemenus = list([
        dict(type="buttons",
             active=-1,
             buttons=list([
                dict(label = 'QB',
                     method = 'update',
                     args = [{'visible': [True, False, False, False]},
                             {'title': 'QB Pass Yards (Yards) vs Wind Speed (mi)',
                              'annotations': []}]
                             ),
                dict(label = 'WR',
                     method = 'update',
                     args = [{'visible': [False,True, False,False]},
                             {'title': 'WR Receiving Yards (Yards) vs Wind Speed (mi)',
                              'annotations': []}]),
                dict(label = 'K',
                     method = 'update',
                     args = [{'visible': [False, False,True, False]},
                             {'title': 'K Field Goal Percentage (%) vs Wind Speed (mi)',
                              'annotations': []}]),
                dict(label = 'RB',
                     method = 'update',
                     args = [{'visible': [False, False, False, True]},
                             {'title': 'RB Rush Yards (Yards)',
                              'annotations': []}]),
                dict(label = 'All',
                     method = 'update',
                     args = [{'visible': [True, True, True, True]},
                             {'title': 'Position Metrics vs Wind Speed (mi)',
                              'annotations': []}]),
                dict(label = 'Reset',
                     method = 'update',
                     args = [{'visible': [True, True, True, True]},
                             {'title': 'Position Metrics vs Wind Speed (mi)',
                              'annotations': []}])
                ]),
            )
        ])
        
    layout = dict(title='Position Metrics vs Wind Speed (mi)',
                  showlegend=False,
                  xaxis=dict(
                        title = 'Wind Speed (mi)'
                        ),
                  yaxis=dict(
                        title = 'Pass Yards (Yds), Receiving Yards (Yds), Rush Yards (Yds), Field Goal Percentage (%)'
                        ),
                updatemenus=updatemenus)

    fig = dict(data=data, layout=layout)
    py.iplot(fig, filename='position_metrics_vs_wind_speed')
    
    
#create graph to measure how humidity has an effect on pass yards, rec yards, field goal percentage, rush yards
def humidity_vs_other():

    humidity_list = merged_data['kickoff_humidity_x'].unique().tolist()
    humidity_list.sort()

    #print(wind_speed_list)
    pass_yds = []
    rec_yds = []
    fgp = []
    rush_yds = []
   
    for percent in humidity_list:
        temp_data = merged_data[merged_data['kickoff_humidity_x'] == percent]
        
        
        qb_data = temp_data[temp_data['position'] == 'QB']
        temp_list = qb_data['pass_yds'].tolist()
        if not temp_list:
            pass_yd_temp_avg = 0

        else:
            pass_yd_temp_avg = mean(temp_list)
            pass_yds.append(pass_yd_temp_avg)

        wr_data = temp_data[temp_data['position'] == 'WR']
        temp_list = wr_data['rec_yds'].tolist()
        if not temp_list:
            rec_yd_temp_avg = 0

        else:
            rec_yd_temp_avg = mean(wr_data['rec_yds'].tolist())
            rec_yds.append(rec_yd_temp_avg)    
            
        k_data = temp_data[temp_data['position'] == 'K']
        temp_list = k_data['fg_perc'].tolist()
        if not temp_list:
            fgp_temp_avg = 0

        else:
            fgp_temp_avg = mean(k_data['fg_perc'].tolist())
            fgp.append(fgp_temp_avg)
        
        rb_data =temp_data[temp_data['position'] == 'RB']
        temp_list = rb_data['rush_yds'].tolist()
        if not temp_list:
            rush_yd_temp_avg = 0

        else:
            rush_yd_temp_avg = mean(rb_data['rush_yds'].tolist())
            rush_yds.append(rush_yd_temp_avg)
    
    #print('passyds')
    #print(pass_yds)
        
    qb = go.Scatter(x=humidity_list,
                              y=pass_yds,
                              name= 'QB Pass Yds',
                              line=dict(color='#33CFA5')
                                        )
                              
    wr = go.Scatter(x=humidity_list,
                              y=rec_yds,
                              name= 'WR Receiving Yds',
                              line=dict(color='orange')
                                        )
    
    k = go.Scatter(x=humidity_list,
                              y=fgp,
                              name= 'K Field Goal Percentage',
                              line=dict(color='blue')
                                        )
                              
    rb = go.Scatter(x=humidity_list,
                              y=rush_yds,
                              name= 'RB Rushing Yds)',
                              line=dict(color='#F06A6A')
                                        )

    
    data = [qb, wr, k, rb]
    #drop_null_wind['wind_intensity'].tolist()
    updatemenus = list([
        dict(type="buttons",
             active=-1,
             buttons=list([
                dict(label = 'QB',
                     method = 'update',
                     args = [{'visible': [True, False, False, False]},
                             {'title': 'QB Pass Yards (Yards) vs Humidity (%)',
                              'annotations': []}]
                             ),
                dict(label = 'WR',
                     method = 'update',
                     args = [{'visible': [False,True, False,False]},
                             {'title': 'WR Receiving Yards (Yards) vs Humidity (%)',
                              'annotations': []}]),
                dict(label = 'K',
                     method = 'update',
                     args = [{'visible': [False, False,True, False]},
                             {'title': 'K Field Goal Percentage (%) vs Humidity (%)',
                              'annotations': []}]),
                dict(label = 'RB',
                     method = 'update',
                     args = [{'visible': [False, False, False, True]},
                             {'title': 'RB Rush Yards (Yards)',
                              'annotations': []}]),
                dict(label = 'All',
                     method = 'update',
                     args = [{'visible': [True, True, True, True]},
                             {'title': 'Position Metrics vs Humidity (%)',
                              'annotations': []}]),
                dict(label = 'Reset',
                     method = 'update',
                     args = [{'visible': [True, True, True, True]},
                             {'title': 'Position Metrics vs Humidity (%)',
                              'annotations': []}])
                ]),
            )
        ])
        
    layout = dict(title='Position Metrics vs Humidity (%)',
                  showlegend=False,
                  xaxis=dict(
                        title = 'Humidity (%)'
                        ),
                  yaxis=dict(
                        title = 'Pass Yards (Yds), Receiving Yards (Yds), Rush Yards (Yds), Field Goal Percentage (%)'
                        ),                    
                updatemenus=updatemenus)

    fig = dict(data=data, layout=layout)
    py.iplot(fig, filename='position_metrics_vs_humidity')
    
    
#create graph to measure how humidity has an effect on receiving yards
    #separated by if the game was played in a dome or not
def rec_yds_humidity_dome():
    
    dome_data = merged_data[merged_data['kickoff_dome_x'] == 'Y']
    no_dome_data = merged_data[merged_data['kickoff_dome_x'] == 'N']
    dome_humidity_list = dome_data['kickoff_humidity_x'].unique().tolist()
    #print(dome_humidity_list)
    for i in range(0, len(dome_humidity_list)):
        dome_humidity_list[i] = dome_humidity_list[i]
    dome_humidity_list.sort()

    no_dome_humidity_list = no_dome_data['kickoff_humidity_x'].unique().tolist()
    #print(no_dome_data)
    for i in range(0, len(no_dome_humidity_list)):
        no_dome_humidity_list[i] = no_dome_humidity_list[i]
    no_dome_humidity_list.sort()

    dome_rec_list = []
    no_dome_rec_list = []
    
    for i in dome_humidity_list:
        humidity_subset = dome_data[dome_data['kickoff_humidity_x'] == i]
        humidity_subset = humidity_subset[humidity_subset['position'] == 'WR']
        rec_list = humidity_subset['rec_yds'].tolist()
        if not rec_list:
            dome_humidity_list.remove(i)
        else:
            avg_rec = mean(rec_list)
            dome_rec_list.append(avg_rec)
        
    for i in no_dome_humidity_list:
        nd_humidity_subset = no_dome_data[no_dome_data['kickoff_humidity_x'] == i]
        nd_humidity_subset = nd_humidity_subset[nd_humidity_subset['position'] == 'WR']
        nd_rec_list = nd_humidity_subset['rec_yds'].tolist()
        #print(nd_rec_list)
        if not nd_rec_list:
            no_dome_humidity_list.remove(i)
            #print('removed')
        else:
            #print('found 1 value')
            avg_rec = mean(nd_rec_list)
            no_dome_rec_list.append(avg_rec)
        
    #print(dome_rec_list)
    #print(no_dome_rec_list)
    
    
    d_rec_yds = go.Scatter(x=dome_humidity_list,
                    y=dome_rec_list,
                    name= 'Receiving Yards in Dome',
                    line=dict(color='blue')
                              )

    nd_rec_yds = go.Scatter(x=no_dome_humidity_list,
                    y=no_dome_rec_list,
                    name= 'Receiving Yards Not in Dome',
                    line=dict(color='#F06A6A', dash = 'dash')
                              
                              )   
                  
    
    data = [d_rec_yds, nd_rec_yds]
    
    updatemenus = list([
        dict(type="buttons",
             active=-1,
             buttons=list([
                dict(label = 'Dome',
                     method = 'update',
                     args = [{'visible': [True, False]},
                             {'title': 'Avg Receiving Yards in Dome',
                              'annotations': []}]
                             ),
                dict(label = 'No Dome',
                     method = 'update',
                     args = [{'visible': [False,True]},
                             {'title': 'Avg Receiving Yards Not in Dome',
                              'annotations': []}]),
                dict(label = 'Both Metrics',
                     method = 'update',
                     args = [{'visible': [False, False]},
                             {'title': 'Avg Receiving Yards',
                              'annotations': []}]),
                dict(label = 'Reset',
                     method = 'update',
                     args = [{'visible': [True, True]},
                             {'title': 'Avg Receiving Yards',
                              'annotations': []}]),    
    
                ]),
            )
        ])
        
    layout = dict(title='Position Metrics vs Humidity',
                  showlegend=False,
                  xaxis=dict(
                        title = 'Humidity (%)'
                        ),
                
                updatemenus=updatemenus)

    fig = dict(data=data, layout=layout)
    py.iplot(fig, filename='position_metrics_vs_humidity_dome')



    