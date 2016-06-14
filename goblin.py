from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.lang import Builder


import numpy as np

kv = '''
<GoblinImage>:
    pos: self.unit.pos
    size: 1,1
'''
Builder.load_string(kv)


class GoblinImage(Image):
    def __init__(self,**kwargs):
        self.unit = kwargs['unit']
        kwargs['source'] = 'game-assets/tiles0.png'
        super(GoblinImage,self).__init__(**kwargs)
        
        data = np.zeros((1,1,3),dtype=np.uint8)
        data[0,0,:] = 255
        data = data.tostring()
        self.texture = Texture.create(size=(1,1), colorfmt="rgb")
        self.texture.blit_buffer(data, colorfmt='rgb', bufferfmt='ubyte')
    

class Goblin(object):
    def __init__(self,_map,name='Gabby'):
        self.map = _map
        self.pos = [_map.elevation.data.shape[0]/2, _map.elevation.data.shape[1]/2 ]
        print self.pos

    def image(self):
        return GoblinImage(unit=self)
