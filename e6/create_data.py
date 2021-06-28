# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 01:08:51 2021

@author: Vaibhav 301386847
"""
import time
import pandas as pd
import numpy as np
from implementations import all_implementations

data = pd.DataFrame(columns=['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort'], index = np.arange(100))

for i in range(100):
    random_array = np.random.randint(-5000,5000,size = 10000)
    for sort in all_implementations:
        st = time.time()
        res = sort(random_array)
        en = time.time()
        data.iloc[i][sort.__name__] = en - st
        

data.to_csv('data.csv', index=False)