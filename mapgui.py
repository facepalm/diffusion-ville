from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

import numpy as np

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
        
    
    def process_map(self,_map):
        self.map = _map
        self.buffer = np.zeros((_map.mapsize_y,_map.mapsize_x,4),dtype=np.float32)
        self.buffer[:,:,0] = np.transpose(_map.elevation.data.copy())
        self.buffer[:,:,1] = np.transpose(_map.vegetation.data.copy())
        self.buffer[:,:,3] = np.ones((_map.mapsize_y,_map.mapsize_x),dtype=np.float32)
        
        self.data = self.float2uint(self.buffer).tostring()
        
        self.texture = Texture.create(size=(_map.mapsize_x, _map.mapsize_y), colorfmt="rgba")
        self.texture.blit_buffer(self.data, colorfmt='rgba', bufferfmt='ubyte')
        #relaod map
        self.parent.scale=4.0
        print _map
