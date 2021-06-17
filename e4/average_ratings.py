# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 17:32:51 2021

@author: vaibhav 301386847
"""

import sys
import pandas as pd
import difflib

filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = sys.argv[3]

movies = open(filename1).readlines()
ratings = pd.read_csv(filename2)

def get_title(movie_name):
    return difflib.get_close_matches(movie_name,movies)

ratings['title'] = ratings['title'].apply(lambda x: get_title(x))
#source https://stackoverflow.com/questions/38147447/how-to-remove-square-bracket-from-pandas-dataframe
ratings['title'] = ratings['title'].str[0]

ratings = ratings.groupby(by=["title"], dropna=True).mean()

ratings['rating'] = ratings['rating'].round(2)

ratings.to_csv(filename3)