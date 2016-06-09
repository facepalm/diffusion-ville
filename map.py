import numpy as np
import cv2
import skimage.filters
import random


default_size = [200,300]

class Map(object):
    def __init__(self, size=default_size):
        self.size = size
        
        self.geography = Layer(self.size)
        
        self.layer = dict()
        self.layer['Pixies'] = ScentLayer(self.size)

    def update(self,dt=0):
        for v in self.layer.values():
            v.update(dt)

class Layer(object):
    def __init__(self, size=default_size):
        self.size=size
        self.data = np.zeros(self.size,np.float32)

    def random_addition(self):
        rx = random.randint(100,150)
        ry = random.randint(100,150)
        
        self.data[rx,ry] += 1
        
    def update(self,dt=0):
        pass

class ScentLayer(Layer):
    def update(self,dt=0):
        self.data *= 0.998
        self.data = skimage.filters.gaussian(self.data,2)
        


m = Map()

while True:
    m.layer['Pixies'].random_addition()
    m.update(1)
    
    cv2.imshow('field', m.layer['Pixies'].data)
    cv2.waitKey(1)
