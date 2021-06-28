# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 19:43:02 2021

@author: Vaibhav 301386847
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv("data.csv")

print(" sorting (speed)    Mean") 
print(data.describe().loc['mean',:].sort_values().to_string())

anova = stats.f_oneway(data['qs1'], data['qs2'], data['qs3'], data['qs4'], data['qs5'], data['merge1'], data['partition_sort'])
print("ANOVA p-value = ", round(anova.pvalue, 2)) #pvalue < 0.05, we must reject the null hypothesis

x_melt = pd.melt(data)
posthoc = pairwise_tukeyhsd(
    x_melt['value'], x_melt['variable'],
    alpha=0.05)

fig = posthoc.plot_simultaneous()