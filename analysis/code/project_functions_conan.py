#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# calculate number of male medals won
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def male_medals(df, search_str, col1, col2):

    mask = df.apply(lambda row: search_str in row.values, axis=1)
    df.loc[mask, "medal_combined_bysex"] = df[col1] - df[col2]

