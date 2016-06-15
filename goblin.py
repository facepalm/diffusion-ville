from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.lang import Builder

import random
import numpy as np

import util

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
        
        data = np.zeros((1,1,4),dtype=np.uint8)
        red = 40- random.randint(0,40)
        data[0,0,:] = [red,140,40-red,255]
        data = data.tostring()
        self.texture = Texture.create(size=(1,1), colorfmt="rgba")
        self.texture.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
        
        
    def refresh(self):
        self.pos=self.unit.pos        
    

class Goblin(object):
    def __init__(self,_map,name='Gabby'):
        self.map = _map
        self.myimage = None
        self.id = util.register(self)
        pos = np.array(_map.elevation.data.shape) /2
        pos[0] += random.randint(-30,30)
        pos[1] += random.randint(-30,30)
        self.pos = [ int(pos[0]),int(pos[1]) ]
        
        #skills
        self.skills = { 'Strength': random.randint(1,3), 'Subtlety': random.randint(1,3), 'Smarts': random.randint(1,3) }
        
        
    def wander(self,dist=2):
        self.walk(random.randint(-2,2),random.randint(-2,2))
            
    def walk(self,dx,dy):
        self.pos[0] += dx
        self.pos[1] += dy
                

    def image(self):
        if self.myimage is not None: return self.myimage
        self.myimage = GoblinImage(unit=self)
        return self.myimage
        
    def update(self,dt):
        self.map.deposit_scent('Goblin',self.pos,dt)
        self.wander()
        self.myimage.refresh()
