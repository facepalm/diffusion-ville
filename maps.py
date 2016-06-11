import numpy as np
import cv2
import skimage.filters
import skimage.morphology
import random

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


default_size = [200,300]

kv = '''
<MapScreen@Screen>:
    name: 'genericname'
    ScrollView:        
        id: mapscroll
           
'''

Builder.load_string(kv)

class MapScreen(Screen):
    pass

class Map(GridLayout):
    
    def __init__(self, **kwargs):
        _size = kwargs['_size'] if '_size' in kwargs else default_size
        self.mapsize_x = _size[0]
        self.mapsize_y = _size[1]
        
        self.elevation = Layer([self.mapsize_x,self.mapsize_y])
        
        self.vegetation = Layer([self.mapsize_x,self.mapsize_y])
        
        self.layer = dict()
        self.layer['Pixies'] = ScentLayer([self.mapsize_x,self.mapsize_y])
        
        super(Map, self).__init__(**kwargs) 
        
        self.rows = self.mapsize_y
        self.cols = self.mapsize_x
        self.size_hint = (None, None)
        self.size = self.mapsize_x*64,self.mapsize_y*64

    def update(self,dt=0):
        for v in self.layer.values():
            v.update(dt)

class Layer(object):
    def __init__(self, size=default_size):
        self.size=size
        self.data = np.zeros(self.size,np.float32)

    def random_addition(self):
        rx = random.randint(0,self.data.shape[0]-1)
        ry = random.randint(0,self.data.shape[1]-1)
        
        self.data[rx,ry] += 1
        
    def randomize(self,distribution='linear',scale=10):     
        if distribution=='pareto':
            self.data= np.random.pareto(scale,self.data.shape)
        else: #random distribution
            self.data= np.random.random_sample(self.data.shape)

    def bloom(self,mask=None):
        '''Bounded diffusion which combines diffusion and dilation to spread pixels.'''
        self.diffuse(2)
        self.data = skimage.morphology.dilation(self.data)
        if mask is not None: self.data = np.minimum(self.data,mask)
        #self.data [self.data < 0] = 0

    def diffuse(self,scale=2):
        self.data = skimage.filters.gaussian(self.data,scale)
    
        
    def update(self,dt=0):
        pass

class ScentLayer(Layer):
    def update(self,dt=0):
        self.data *= 0.998
        self.data = skimage.filters.gaussian(self.data,2)
    
    
        
        
if __name__ == "__main__":

    m = Map()

    while True:
        m.layer['Pixies'].random_addition()
        m.update(1)
        
        cv2.imshow('field', m.layer['Pixies'].data)
        cv2.waitKey(1)