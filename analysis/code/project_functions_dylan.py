import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def sportpopularity(data, *args):
    """
    Returns a dataframe with only the passed-in sports.
    
    Parameters:
    -----------
    data:
        The dataframe to extract information from.
        
    *args:
        Any number of sport names that you wish to look at.
        
    Returns
    -------
    Dataframe
    """
    
    sports = []
    for i in args:
        sports.append(i)
        
    isolated_sports_df = data[data['discipline_title'].isin(sports)]
    
    isolated_sports_df = isolated_sports_df.rename(columns={'discipline_title' : 'Sport', 
                                    'medal_type' : 'Medal Won',
                                    'event_title' : 'Sport Event',
                                    'athlete_full_name' : 'Athlete Name', 
                                    'first_game' : 'First Game',
                                    'country_name' : 'Home Country',
                                    'game_location' : 'Host Country', 
                                    'game_name' : 'Game Name',
                                    'game_season' : 'Game Season',
                                    'game_year' : 'Year'})
    isolated_sports_df = isolated_sports_df.reset_index(drop=True)
    
    return isolated_sports_df