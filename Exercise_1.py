#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 21:13:18 2020

@author: maritkollstuen
"""

import requests
import pandas as pd
import json

# Import JSON data
url = 'https://api.npolar.no/marine/biology/sample/?q=&fields=expedition,utc_date,programs,conveyance&limit=all&format=json&variant=array'
data = requests.get(url).json()
column_names = data.pop(0)


# Convert to Pandas DataFrame
df = pd.DataFrame(data, columns = column_names)
df['utc_date'] = pd.to_datetime(df['utc_date'])
df = df.sort_values(by=['expedition', 'utc_date'])

# Extract unique expeditions and their start- and end date
# Assumed the first program and vessel are the same throughout the expetition
df_to_json = df.groupby('expedition')['utc_date'].agg(['first',
                       'last']).rename(columns={'first':'start_date',
                       'last':'end_date'})
df_to_json['programs'] = df.groupby('expedition')['programs'].agg('first')
df_to_json['conveyance'] = df.groupby('expedition')['conveyance'].agg('first')

# Convert back to JSON
result = df_to_json.to_json(orient = "index")
parsed = json.loads(result)
json.dumps(parsed, indent = 4)