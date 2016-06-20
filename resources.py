import util
import math
import numpy as np
import random

class ResourceModel(object):
    pass
    


class Resource(object):
    def __init__(self,name):
        self.id = util.register(self)
        self.name = name
        self.amount = 0
        self.supply = 1.
        self.demand = 1.
        self.price = 1.
        self.tc = 3600. 
        
    def update(self,dt):
        diffsum = (self.demand - self.supply)/(self.demand + self.supply)
        frac = math.exp(-dt/self.tc)
        self.supply *= frac
        self.demand *= frac
        self.price *= 1.0 + 0.1*diffsum*dt/self.tc
        
        '''self.tc *= 0.99*(3600 - dt)/3600
        
        if abs(diffsum) > 0.9: 
            self.tc *= 1.1 
            self.tc += 3600'''
        #elif abs(diffsum) < 0.1:
        #    self.tc *= 0.9


#testing            
if __name__ == "__main__":
    test = Resource('Test')
    
    for i in range(10000):
        #test.supply += random.random()
        #test.demand += 2*random.random()
        if random.random() > 0.4:
            test.supply += 1
        if random.random() > 0.5:
            test.demand += 1            
        print test.supply, test.demand, test.price, test.tc
        test.update(60)
        
