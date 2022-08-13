# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 19:10:47 2022

@author: mubar
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('eda_data.csv')

# choose relevant columns

df.columns

df_models = df[['avg_salary', 'Rating', 'Size', 'Founded',
       'Type of ownership', 'Industry', 'Sector', 'Revenue', 'num_comp', 'hourly', 'employer_provided', 'state', 'same_state', 'age', 'python_yn', 'sql_yn',
       'spark', 'power_bi', 'excel', 'job_simp', 'seniority']]

# get dummy data 

df_dum = pd.get_dummies(df_models)

# train test split

from sklearn.model_selection import train_test_split

X = df_dum.drop('avg_salary', axis=1)
y = df_dum.avg_salary

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# multiple linear regression

import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm, X_train, y_train, scoring="neg_mean_absolute_error" ,cv=3))

# lasso regression

lm_l = Lasso(alpha=0.1)
lm_l.fit(X_train, y_train)
np.mean(cross_val_score(lm_l, X_train, y_train, scoring="neg_mean_absolute_error" ,cv=3))

alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring="neg_mean_absolute_error" ,cv=3)))
    
plt.plot(alpha, error)
err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns= ['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]

# random forest

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
np.mean(cross_val_score(rf, X_train, y_train, scoring="neg_mean_absolute_error" ,cv=3))

# tune models GrisearchCV

from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto', 'sqrt', 'log2')}

gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

# test ensembles

tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_lml)
mean_absolute_error(y_test,tpred_rf)

mean_absolute_error(y_test,(tpred_rf+tpred_lml)/2)