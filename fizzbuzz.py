#def F(n):
#    if n < 2:
#        print ("fib({0})".format(n));
#        return n
#    else:
#        print ("fib({0}) = fib({1}) + fib({2})".format(n,n-2,n-1))
#        return F(n-2) + F(n-1)
        
  
        
for x in range(1,101):
    output = ''
    if x % 3 == 0:
        output += 'Fizz'
    if x % 5 == 0:
        output += 'Buzz'
    if output == '':
        output = x
    
    print output