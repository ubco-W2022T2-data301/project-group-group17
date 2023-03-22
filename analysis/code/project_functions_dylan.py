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
                                  'event_title' : 'Sporting Event Name',
                                  'game_location' : 'Olympic Host',
                                  'game_name' : 'Olympic Name',
                                  'game_year' : 'Year'})
    isolated_sports_df = isolated_sports_df.reset_index(drop=True)
    
    return isolated_sports_df