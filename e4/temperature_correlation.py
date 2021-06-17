# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 21:56:43 2021

@author: Vaibhav 301386847
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = sys.argv[3]

stations = pd.read_json(filename1, lines=True)
stations['avg_tmax'] = stations['avg_tmax']/10

cities =pd.read_csv(filename2)
cities.dropna(inplace=True)


cities['area'] = cities['area']/1000000
cities = cities[cities.area <= 10000] #10000km2 = 10000000000m2
cities['density'] = cities['population']/cities['area']

cities.reset_index(drop=True)

def distance(city, stations):
    dlat = np.deg2rad(stations['latitude']-city['latitude'])
    dlong = np.deg2rad(stations['longitude']-city['longitude'])
    a = np.sin((dlat)/2.0)**2 + np.cos(np.deg2rad(city['longitude'])) * np.cos(np.deg2rad(stations['longitude'])) * np.sin((dlong)/2.0)**2
    return 6371*np.arcsin(np.sqrt(a))*2
    
def best_tmax(city, stations):
    stations['dist'] = distance(city, stations)
    return stations.iloc[np.argmin(stations['dist'])].avg_tmax
    
cities['tmax'] = cities.apply(best_tmax, axis = 1, stations=stations)
    
plt.scatter(cities['tmax'],cities['density'])
plt.title("Temperature vs Population Density")
plt.xlabel("Avg Max Temperature (\u00b0C)")
plt.ylabel("Population Density (people/km\u00b2)")

plt.savefig(filename3)