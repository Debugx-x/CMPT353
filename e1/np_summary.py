import numpy as np
data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

print("Row with lowest total precipitation:")
totalsum = totals.sum(axis = 1)
print(np.argmin(totalsum))

print("Average precipitation in each month:")
precipitation_month = totals.sum(axis = 0)
observation_month = counts.sum(axis = 0)
print(precipitation_month/observation_month)

print("Average precipitation in each city:")
precipitation_city = totals.sum(axis = 1)
observation_city = counts.sum(axis = 1)
print(precipitation_city/observation_city)

print("Quarterly precipitation totals:")
no_rows = np.shape(totals)[0]
trans = np.reshape(totals,(4*no_rows,3))
trans = trans.sum(axis =1)
trans = np.reshape(trans,(no_rows,4))
print(trans)