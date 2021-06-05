# -*- coding: utf-8 -*-
"""
Created on Mon May 24 23:45:07 2021

@author: vaibhav 

"""

import sys
import matplotlib.pyplot as plt
import pandas as pd

file1 = sys.argv[1]
file2 = sys.argv[2]

arg1 = pd.read_csv(file1, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

arg1.sort_values(by=['views'],inplace=True, ascending=False)

views = arg1['views'].values
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.title("Distribution of Views")
plt.xlabel("Ranks")
plt.ylabel("Views")
plt.plot(views)

arg2 = pd.read_csv(file2, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

arg2['views1'] = arg1['views']

plt.subplot(1,2,2)
plt.title("Daily Views")
plt.xlabel("day 1 Viewers")
plt.ylabel("day 2 Viewers")
plt.xscale('log')
plt.yscale('log')
plt.scatter(arg2['views1'],arg2['views'])

plt.savefig('wikipedia.png')