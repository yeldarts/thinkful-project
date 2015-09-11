import collections
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd

def handleData (data, name):
    #Handle the frequencies
    c = collections.Counter(data)
    count_sum = sum(c.values())
    with open(name + '_frequency.csv','w') as outputFile:
        outputFile.write('Number,Frequency\n')
        for k,v in c.iteritems():
            outputFile.write(str(k) + ',' + str(float(v) / count_sum) + '\n')
    
    plt.close()
    
    plt.boxplot(data)
    plt.savefig(name + "_boxplot.png")
    
    plt.close()
    
    plt.hist(data, histtype='bar')
    plt.savefig(name + "_hist.png")
    
    plt.close()
    
    plt.figure() 
    graph1 = stats.probplot(data, dist="norm", plot=plt)
    plt.savefig(name + "_probplot.png")
    
    
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
#removes empty lines
loansData.dropna(inplace=True)
#loansData.boxplot(column='Amount.Funded.By.Investors',return_type='dict')
handleData(loansData['Amount.Requested'].values.tolist(), 'Lending_Club')
