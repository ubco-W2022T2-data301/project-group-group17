import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.colors as mcolors
import seaborn as sns

def medalCounts(df, medal_type):
    """
    The function denoted as "medalCounts" returns a dataframe with a series of parameters associated with a unique medal type. 
    Please refer to the parameters and returns section for more information.
    Please note, that if the medal type is spelt incorrectly, the function will not run.
    
    Parameters:
    -----------
    df: dataframe
        The dataframe to extract information from.
        
    medal_type: string
        The specific medal type of interest,
        
    Returns
    -------
        Returns a new dataframe which is subsetted to only contain the following parameters:
            - Country
            - Medal Type
            - Country Code
            - Specific Medal Type Count
    """
    
    dfmedal_count = df[df["medal_type"] == medal_type.upper()]
    
    dfmedal_count = (dfmedal_count.groupby(by=['country','medal_type', 'country_code'])[['game_year']].count()
     .rename(columns = {"medal_type":"Medal", "game_year" : medal_type+"_Medal_Count"})
     .sort_values(str(medal_type)+"_Medal_Count" , ascending=False)
     .reset_index())
     
    return dfmedal_count