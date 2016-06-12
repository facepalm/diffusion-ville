from assets import *
from kivy.uix.image import Image


class Tile(Image):
    #pressed = ListProperty([0, 0])
    
    def __init__(self,**kwargs):
        self.index = kwargs['index'] if 'index' in kwargs else (0,0)      
        self.texture = TEX_GRASS
        super(Tile, self).__init__(source=self.source, **kwargs)
        
    def reload_texture(self):
        if not self.parent: return
        veg = self.parent.vegetation.data[self.index]        
        elev = self.parent.elevation.data[self.index]        
        
        print veg, elev, self.index
        
        if veg > 1.0:
            self.texture = TEX_TREE
        elif veg > 0.5:
            self.texture = TEX_BUSH    
