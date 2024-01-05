# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:01:01 2022

@author: sgirt
"""

#with open(0) as data_in:
with open('sample.txt') as data_in:
    data = data_in.read().splitlines()

# Get parameters 
params = data.pop(0).split()
n = params[0]
k = params[1]
m = params[2]


# Create dictionary of location ids and long/lat coordinates
#loc_id = {i : data[i] for i in range(0, len(data))}

longitude = {}
latitude = {}

