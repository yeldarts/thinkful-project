import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt 

print 'Preparing the dataset...'

# TODO: load data directly from website
loans = pd.read_csv("LoanStats3d.csv")

# subset a smaller DF of only needed data
loansDF = pd.DataFrame(columns = ['int_rate', 'annual_inc', 'home_ownership'])
loansDF['int_rate'] = loans.int_rate
loansDF['annual_inc'] = loans.annual_inc.astype(float)
loansDF['home_ownership'] = loans.home_ownership

# drop any rows with missing values
loansDF.dropna(inplace=True)

# reformat interest rate. drop '%' sign and convert to float
loansDF['int_rate'] = map(lambda x: float(x[:x.find('%')]), loansDF['int_rate'])

print 'Building model #1...'

# include intercept in data
loansDF['Intercept'] = float(1.0)

# fit the model
model = sm.OLS(loansDF['int_rate'], loansDF[['Intercept', 'annual_inc']])
result = model.fit()

print '~~~~~~ MODEL 1 ~~~~~~' 
print result.summary()

# Add home_ownershipership to model
loansDF['home_ownership'] = pd.Categorical(loansDF.home_ownership).codes

model2 = sm.OLS(loansDF['int_rate'], loansDF[['Intercept', 'annual_inc', 'home_ownership']])
result2 = model2.fit()

print '~~~~~~ MODEL 2 ~~~~~~' 
print result2.summary()

# Add interaction term between annual_inc and home ownsership
loansDF['Interaction'] = loansDF['annual_inc'] * loansDF['home_ownership']

model3 = sm.OLS(loansDF['int_rate'], loansDF[['Intercept', 'annual_inc', 'home_ownership', 'Interaction']])
result3 = model3.fit()

print '~~~~~~ MODEL 3 ~~~~~~' 
print result3.summary()