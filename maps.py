import numpy as np
import cv2
import skimage.filters
import skimage.morphology
import random

default_size = [222,222]
scale = 1.0

class Map(object):
    
    def __init__(self, **kwargs):
        size = kwargs['size'] if 'size' in kwargs else default_size
        self.mapsize_x = size[0]
        self.mapsize_y = size[1]
        
        self.elevation = Layer([self.mapsize_x,self.mapsize_y])
        
        self.vegetation = Layer([self.mapsize_x,self.mapsize_y])
        
        self.layer = dict()
        self.layer['Pixies'] = ScentLayer([self.mapsize_x,self.mapsize_y])
        
        #super(Map, self).__init__(**kwargs) 
        
        '''self.rows = self.mapsize_y
        self.row_default_height=16
        self.cols = self.mapsize_x
        self.col_default_width=16
        
        self.size_hint = (None, None)
        self.size = self.mapsize_x*16*scale,self.mapsize_y*16*scale

        for x in range(0,10):#self.mapsize_x-1):
            for y in range(0,10):# self.mapsize_y-1):
                print (x,y)
                mapt = tile.Tile(index=(x,y),allow_stretch=False,size_hint=(None, None))
                #mapt = Image(source='game-assets/tiles_forest.png')
                self.add_widget(mapt)  
                mapt.reload_texture()                  '''

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
