#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 21:11:28 2020

@author: maritkollstuen
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 17:39:02 2020

@author: maritkollstuen
"""

import requests
import urllib.request, json

import xarray as xr
import netCDF4
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


def create_df(url, depth):
    """
    Function that gathers the permafrostdata from the different 
    depths in one dataframe
    
    Input: <string> url
    Output: <DataFrame> Pandas DataFrame
    """
    f = requests.get(url).json()
    data = f.pop(0)
    
    df = pd.DataFrame(data['data'])
    df['when'] = pd.to_datetime(df['when'])
    df = df.set_index('when')
    df = df.rename(columns={'value':str(depth)})
    return df

if __name__ == '__main__':

    # Import data:
    url_15m = u'https://api.npolar.no/indicator/timeseries/?facets=label.en&q=&filter-systems=mosj.no&filter-authors.@id=met.no&filter-keywords.@value=land&filter-locations.placename=Janssonhaugen&filter-label.en=15+m&format=json&variant=array&limit=1'
    url_25m = u'https://api.npolar.no/indicator/timeseries/?facets=label.en&q=&filter-systems=mosj.no&filter-authors.@id=met.no&filter-keywords.@value=land&filter-locations.placename=Janssonhaugen&filter-label.en=25+m&format=json&variant=array&limit=1'
    url_40m = u'https://api.npolar.no/indicator/timeseries/?facets=label.en&q=&filter-systems=mosj.no&filter-authors.@id=met.no&filter-keywords.@value=land&filter-locations.placename=Janssonhaugen&filter-label.en=40+m&format=json&variant=array&limit=1'

    # Create pandas DataFrame
    df15 = create_df(url_15m, '15 m')
    df25 = create_df(url_25m, '25 m')
    df40 = create_df(url_40m, '40 m')
    df = df15.merge(df25, on = 'when').merge(df40, on = 'when')
    
    # Visualization
    fig, ax = plt.subplots()
    df.plot(color = ['blue', 'red', 'green'], ax = ax)
    ax.yaxis.set_tick_params(which='major', labelcolor='blue')
    fig.suptitle('Ground temperature in permafrost, Janssonhaugen', size = 12)
    ax.yaxis.grid()
    ax.minorticks_off()
    ax.set_ylim(-6.5, -4.25)
    ax.set_ylabel(r'Temperature $^{\circ}$C', color = 'blue')
    ax.set(xlabel = None)
    ax.legend(loc = 'lower center', bbox_to_anchor = (0.5,-0.3), ncol = 3, frameon = False)
    sns.despine(left=True, right=True)
    plt.savefig('Exercise_2.png', bbox_inches = 'tight')
    
