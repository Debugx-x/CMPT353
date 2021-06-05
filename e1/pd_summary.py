import pandas as pd
totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

print("Row with lowest total precipitation:")
rowsum = totals.sum(axis = 1)
print(rowsum.idxmin(axis=0))

print("Average precipitation in each month:")
precipitation_month = totals.sum(axis = 0)
observation_month = counts.sum(axis = 0)
print(precipitation_month/observation_month)

print("Average precipitation in each city:")
precipitation_city = totals.sum(axis = 1)
observation_city = counts.sum(axis = 1)
print(precipitation_city/observation_city)