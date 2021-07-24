# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 20:44:22 2021

@author: Vaibhav 301386847
"""

import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier

labelled_data = pd.read_csv(sys.argv[1])
unlabelled_data = pd.read_csv(sys.argv[2])

X = labelled_data.loc[:,'tmax-01':'snwd-12']
y = labelled_data['city']

X_unlabelled = unlabelled_data.loc[:,'tmax-01':'snwd-12']

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=10))

model.fit(X_train, y_train)

predictions = model.predict(X_unlabelled)
print("Score :", round(model.score(X_test, y_test), 3))

df = pd.DataFrame({'truth': y_test, 'prediction': model.predict(X_test)})
#print(df[df['truth'] != df['prediction']])

pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)