from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

import numpy as np

from maps import Layer

kv = '''
<MapScreen@Screen>:
    name: 'map name'    
    Scatter:
        id: mapscale
        FloatLayout:
            id: maplayout
        MapImage:
            id: mapimg
            allow_stretch: False                        
           
'''

Builder.load_string(kv)

class MapScreen(Screen):
    pass

class MapImage(Image):        

    def __init__(self,**kwargs):
        pass#self.blit_texture = Texture.create(size=(100, 100), colorfmt='rgba')
        self.buffer = None
        super(MapImage,self).__init__(**kwargs)
        
    def float2uint(self,buf):
        out32 = buf.copy()
        out32[out32 < 0 ] = 0
        out32[out32 > 1 ] = 1
        #out32 /= out32.max()        
        out32 *= 255
        return out32.astype(np.uint8)
        
    
    def refresh_map(self):
        #no reloading, just redrawing

        veg = np.transpose(self.map.vegetation.data.copy())        
        veg[veg < 0] = 0
        self.buffer = self.baseimg.copy()        
        self.buffer[veg > 0,0] *= 0.5
        self.buffer[:,:,1] += (veg/2)
        
        data = self.float2uint(self.buffer).tostring()
        
        self.texture.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
        
    
    def process_map(self,_map):
        self.parent.scale=16.0
        self.parent.pos = (-750+_map.mapsize_y/2,-750+_map.mapsize_x/2)
        self.map = _map
        
        self.bumps = Layer([_map.mapsize_y,_map.mapsize_x])
        self.bumps.randomize()
        
        self.buffer = np.zeros((_map.mapsize_y,_map.mapsize_x,4),dtype=np.float32)
        elev = np.transpose(_map.elevation.data.copy())
        #self.buffer[:,:,1] = np.transpose(_map.vegetation.data.copy())
        #self.buffer[:,:,3] = np.ones((_map.mapsize_y,_map.mapsize_x),dtype=np.float32)
        
        self.baseimg = np.zeros((_map.mapsize_y,_map.mapsize_x,4),dtype=np.float32)
        self.baseimg[:,:,3] = np.ones((_map.mapsize_y,_map.mapsize_x),dtype=np.float32)
        r = np.zeros((_map.mapsize_y,_map.mapsize_x),dtype=np.float32)
        g = np.zeros((_map.mapsize_y,_map.mapsize_x),dtype=np.float32)
        b = np.zeros((_map.mapsize_y,_map.mapsize_x),dtype=np.float32)
        tree_line=20
        r[elev <= tree_line] = 0.46
        r[elev > tree_line] = 0.33
        g[elev <= tree_line] = 0.15
        g[elev > tree_line] = 0.33
        b[elev <= tree_line] = 0.05
        b[elev > tree_line] = 0.33
        self.baseimg[:,:,0] = np.multiply(r,1+.2*self.bumps.data)
        self.baseimg[:,:,1] = np.multiply(g,1+.2*self.bumps.data)
        self.baseimg[:,:,2] = np.multiply(b,1+.2*self.bumps.data)
                
        #basedata = self.float2uint(self.baseimg).tostring()
        
        #self.data = self.float2uint(self.buffer).tostring()
        
        self.texture = Texture.create(size=(_map.mapsize_x, _map.mapsize_y), colorfmt="rgba")
        #self.texture.blit_buffer(basedata, colorfmt='rgba', bufferfmt='ubyte')
        self.refresh_map()

        print self.parent.x, self.parent.y
