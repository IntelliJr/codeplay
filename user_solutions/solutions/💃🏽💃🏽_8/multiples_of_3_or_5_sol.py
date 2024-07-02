# find the sum of all multiples of 3 or 5 below the number passed in: 


def multiples_of_3_or_5(num):
    numlist = []
    i=0
    if(num>0):
        
        while (i<num):
            if (i%3==0 or i%5==0): 
                numlist.append(i)
            i+=1    
        sumoflist = sum(numlist)
        
        return sumoflist
    else:
        return 0