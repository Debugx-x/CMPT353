# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 19:51:58 2021

@author: vaibh
"""

import sys
import pandas as pd
import numpy as np
from pykalman import KalmanFilter
from xml.dom.minidom import parse

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def read_gpx(data_filename):
    data = parse(data_filename)
    trkpt = data.getElementsByTagName("trkpt")
    lat = []
    long = []
    for i in trkpt:
        lat.append(i.getAttribute('lat'))
        long.append(i.getAttribute('lon'))
    points = pd.DataFrame()
    points['lat'] = lat
    points['lon'] = long
    points['lat'] = points['lat'].astype(float)
    points['lon'] = points['lon'].astype(float)
    return points

#source: https://stackoverflow.com/questions/40452759/pandas-latitude-longitude-to-distance-between-successive-rows
def haversinecalc(lat, long, lat2, long2):
    dlat = np.deg2rad(lat2-lat)
    dlong = np.deg2rad(long2-long)
    a = np.sin((dlat)/2.0)**2 + np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(lat2)) * np.sin((dlong)/2.0)**2
    return 6371*np.arcsin(np.sqrt(a))*2

def distance(points):
    data = points.copy()
    data['shifted_lat'] = data['lat'].shift(periods = 1)
    data['shifted_lon'] = data['lon'].shift(periods = 1)
    data['dist'] = data.apply(lambda x: haversinecalc(x['lat'], x['lon'], x['shifted_lat'], x['shifted_lon']), axis = 1)
    return data['dist'].sum()

def smooth(points):
    initial_state = points.iloc[0]
    observation_covariance = np.diag([0.85,0.85]) ** 2 
    transition_covariance = np.diag([0.5,0.5]) ** 2 
    transition = [[1,0],[0,1]]
    kf = KalmanFilter(initial_state_mean = initial_state, observation_covariance = observation_covariance, transition_covariance = transition_covariance, transition_matrices = transition)
    kalman_smoothed, _ = kf.smooth(points)
    df = pd.DataFrame(kalman_smoothed)
    df = df.rename(columns={0: "lat", 1: "lon"})
    return df

def main():
    points = read_gpx("walk1.gpx")
    print('Unfiltered distance: %0.2f' % (distance(points)))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points)))
    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()