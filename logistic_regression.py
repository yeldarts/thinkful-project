import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import math
loansData = pd.read_csv('loansData_clean.csv')

def logistic_function(coeff,fico,loanAmount,intRate):
	print "Interest Rate = " + str(intRate)
	print "FICO Score = " + str(fico)
	print "FICO Coefficient = " + str(coeff[2])
	print "Amount Requested = " + str(loanAmount)
	print "Amount Requested Coefficient = " + str(coeff[1])
	
	p = 1/(1 + math.exp(1.0 + (coeff[2]*fico) + (coeff[1]*loanAmount)))
	print "Probability of obtaining loan: " + str(p)
	if (p < 0.30):
		print 'Loan Funded.'
	else:
		print 'Loan Not Funded.'

print loansData['Interest.Rate'][0:5]

print loansData['Loan.Length'][0:5]

print loansData['FICO.Range'][0:5] 

print "cleaning time"
interestRateLimit = 0.12
createCheckRate = loansData['Interest.Rate'].map(lambda x: x <= interestRateLimit)
print "type"
print type(createCheckRate)
print "first 5"
print createCheckRate[0:5]
loansData['IR_TF'] = createCheckRate

print "new IR_TF"
print loansData['IR_TF'][0:5]

intercept = 1.0

loansData['Intercept'] = 1.0

df = pd.DataFrame(loansData)
print "interest rate < 0.10"
print df[df['Interest.Rate'] <= interestRateLimit].head() # should all be True
print "interest rate > 0.13"
print df[df['Interest.Rate'] >= interestRateLimit].head() # should all be False



ind_vars = ['Intercept','Amount.Requested','FICO.Score']

logit = sm.Logit(df['IR_TF'], df[ind_vars])
result = logit.fit()
coeff = result.params
print coeff

logistic_function(coeff,750,10000,interestRateLimit)
