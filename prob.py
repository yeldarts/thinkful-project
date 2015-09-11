import collections
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt

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
    
    
# Sample List  
print "Starting the Sample List"
x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]
handleData(x,'sample_list')

# Random Normal
print "Starting the Random Normal"
test_data = np.random.normal(size=1000)   
handleData(test_data,'random_normal')

# Random Uniform
print "Starting the Random Uniform"
test_data2 = np.random.uniform(size=1000)   
handleData(test_data2,'random_uniform')                   





loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')