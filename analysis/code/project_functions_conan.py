#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#------------------------------------------------------------------------------------------------------------------------------------------#

# calculate number of male medals won
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

#------------------------------------------------------------------------------------------------------------------------------------------#
### Q1 Functions ####

# Q1 load and proccess data function 
def q1_load_process(url_or_path_to_csv_file):
    
    df_medals = pd.read_csv(url_or_path_to_csv_file)
    
    df = df_medals
    
    df = (df.drop(['event_title', 'participant_title', 'athlete_url', 'athlete_full_name', 'country_code', 'country_3_letter_code'], axis = 'columns')
          .assign(slug_game=df['slug_game'].str[-4:])
          .rename(columns={'slug_game': 'year'})
          .reset_index())
    
    df = (df.drop(['index'], axis = 'columns')
          .assign(medal_bysex=df.groupby(['medal_type', 'event_gender', 'country_name', 'year'])['medal_type'].transform('count'),
                  medal_all_bysex=df.groupby(['event_gender', 'country_name', 'year'])['medal_type'].transform('count'),
                  medal_total=df.groupby(['medal_type', 'country_name', 'year'])['medal_type'].transform('count'),
                  medal_all=df.groupby(['country_name', 'year'])['medal_type'].transform('count')))
    
    df['medal_%'] = ((df['medal_bysex']/df['medal_total'])*100)
    
    return df


# Q1 plot prep function 
def q1_plot_prep(data_frame):
    
    df = data_frame
    
    df = (df.sort_values(by=['medal_all'], ascending = False).groupby('year').head(10).reset_index()
          .drop(['index'], axis= "columns")
          .groupby('country_name', group_keys=False).apply(lambda x: x.loc[x.medal_all.idxmax()]).sort_values('medal_all',ascending = False).groupby('year').head(10))
    
    return df


# calculate male only medals
def male_medals(df, search_str, col1, col2):

    mask = df.apply(lambda row: search_str in row.values, axis=1)
    df.loc[mask, "medal_all_bysex"] = df[col1] - df[col2]
    
    
# caluculate and prepare data frame for final data viz    
def q1_final_analysis(data_frame):
    
    df = data_frame
    df = df[df['event_gender'].str.contains('Open|Mixed' )==False]
    
    df = (df.sort_values(by=['medal_all'], ascending = False).groupby('year').head(10).reset_index()
          .drop(['index'], axis= "columns")
          .groupby('year', as_index=False).apply(lambda x: x.loc[x.medal_all.idxmax()]).sort_values('medal_all',ascending = False).groupby('year').head(1)
          .sort_values(by=['year']))
    
    male_medals(df, 'Women', 'medal_all', 'medal_all_bysex')
    
    return df
    
    
# prepare data frame for final presentation plot
def q1_pres_plot(data_frame):

    df = data_frame
    
    df1 = (df
           .drop(['discipline_title', 'medal_type', 'participant_type', 'medal_bysex', 'medal_total', 'event_gender'], axis='columns')
           .assign(medal_female=df['medal_all'] - df['medal_all_bysex']))
    
    df1 = (df1.assign(medal_diff=df1['medal_all_bysex'] - df1['medal_female'])
           .rename(columns={'year' : 'Year',
                            'country_name' : 'Country',
                            'medal_all_bysex' : 'Male Medal Winners',
                            'medal_all' : 'Total Medals Won',
                            'medal_female' : 'Female Medal Winners',
                            'medal_diff' : 'Male vs Female Diffrence'}))
    
    return df1 

#------------------------------------------------------------------------------------------------------------------------------------------#

#### Q2 Functions ####


# merge dataframes for q2 EDA
def q2_merge(data1, data2):
    
    df1 = data1
    
    ### preparing df_hosts for merge 
    
    df1 = df1.drop(['game_slug', 'game_end_date', 'game_start_date', 'game_name'], axis = 'columns').rename(columns={'game_year' : 'year'})
    
    ### preparing df_medals for merge
    df2 = medal_bysex
    df2['year'] = df2['year'].astype(int)
    
    ### merging both dataframes together
    df_merge = df1.merge(df2, how='inner', on='year')
    
    return df_merge


# q2 final merging and plot preperation 
def q2_plotprep(data1, data2):
    
    df1=data1
    df=data2
    
    df1 = df1.drop(['game_slug', 'game_end_date', 'game_start_date', 'game_name'], axis = 'columns').rename(columns={'game_year' : 'year'})
    df1['counts'] = df1.groupby(['game_location'])['game_location'].transform('count')
    
    df = (df.sort_values(by=['medal_all'], ascending = False).groupby('year').head(1).reset_index()
          .drop(['index'], axis= "columns"))
    
    df_merge = df1.merge(df, how='inner', on='year')
    
    return df_merge

#------------------------------------------------------------------------------------------------------------------------------------------#

#### Q3 Functions ####


# Q3 eda function 
def q3_eda(data1, data2):
    
    df1 = data1.drop(['short_name', 'birth_date', 'country', 'birth_place', 'birth_country', 'country_code', 'discipline', 'discipline_code', 'residence_place', 'residence_country', 'height_m/ft', 'url'], axis= "columns")
    
    df2 = data2
    df2 = (df2[['medal_type', 'athlete_name', 'country', 'discipline']]
           .rename(columns={'athlete_name' : 'name'}))
    
    df_merged = df1.merge(df2, how='inner', on='name')
    
    return df_merged


# Q3 add calcualted columns of male or female athlets sent and total
def q3_calc(data):
    
    df=data
    
    df=(df.drop(['short_name', 'birth_date', 'birth_place', 'birth_country', 'country_code', 'discipline', 'discipline_code', 'residence_place', 'residence_country', 'height_m/ft', 'url'], axis= "columns"))
    
    df=(df.assign(athlete_index = 1))
    
    df=(df.assign(athletes_sent = df.groupby(['country', 'gender'])['athlete_index'].transform('count'),
                  athletes_total = df.groupby(['country'])['athlete_index'].transform('count'))
        .replace(['M','F'],['Male', 'Female']))
    
    df['athlete_%']=((df['athletes_sent']/df['athletes_total'])*100)
    
    return df


# Q3 final plot prep (merging and adding final calculated columns of athlete stats)
def q3_final_plotprep(data1, data2):
    
    df1 = data1.drop(['short_name', 'birth_date', 'birth_place', 'birth_country', 'country_code', 'residence_place', 'residence_country', 'height_m/ft', 'url'], axis= "columns")
    
    df2 = data2
    df2 = (df2[['medal_type', 'athlete_name', 'country', 'discipline']]
           .rename(columns={'athlete_name' : 'name'}))
    
    df_merged = (df1.merge(df2, how='outer', on='name')
                 .drop(['country_y', 'discipline_y'], axis='columns')
                 .rename(columns={'country_x' : 'country',
                                  'discipline_x' : 'discipline'}))
    
    df = df_merged
    
    df['athlete_index'] = 1
    df['athletes_sent'] = (df.groupby(['country', 'gender'])['athlete_index'].transform('count'))
    df['athletes_total'] = (df.groupby(['country'])['athlete_index'].transform('count'))
    df['athlete_%'] = ((df['athletes_sent']/df['athletes_total'])*100)
    df['medal_count'] = (df.groupby(['country', 'gender'])['medal_type'].transform('count'))
    df = df.replace(['M','F'],['Male', 'Female'])
    
    return df

#------------------------------------------------------------------------------------------------------------------------------------------#