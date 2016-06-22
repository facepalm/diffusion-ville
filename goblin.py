from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.lang import Builder

import random
import numpy as np

import image_processing as ip
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
        
        #fiscal data
        self.wealth = 0.0 #money owed by/to the larger community
        self.credit_limit = 0.0 #amount
        
        self.labor = 0 #stored workload
        
        #skills
        self.skills = { 'Strength': random.randint(1,3), 
                        'Subtlety': random.randint(1,3), 
                        'Smarts': random.randint(1,3),
                        'Speed': random.randint(1,3) }
        
        
    def wander(self,dt):
        dist = util.sround(self.skills['Speed']*(dt/60.))
        if dist == 0: return
        px1, px2, py1, py2 = self.pos[0]-dist, self.pos[0]+dist+1,self.pos[1]-dist, self.pos[1]+dist+1
        inds = np.reshape(np.array(range(0,pow(2*dist+1,2))),(2*dist+1,2*dist+1))
        elev = self.map.elevation.data[px1:px2,py1:py2]
        wlth = ip.lognorm(self.map.fetch_scent('Wealth').data[px1:px2,py1:py2])
        gob = ip.lognorm(self.map.fetch_scent('Goblin').data[px1:px2,py1:py2])
        
        heat = np.random.random_sample(elev.shape)
        
        prob = ip.norm(heat+wlth-elev/4-gob)
        prob /= prob.sum()
        
        #print elev
        
        ind = np.random.choice(inds.ravel(),p=prob.ravel())
        i = np.where(inds == ind)
        #print inds, ind
        #print i, i[0], i[1][0]
        
        if self.labor > 1.0:
            self.labor -= self.forage(self.labor - 1.0)
            
        
        self.walk(i[0][0]-dist,i[1][0]-dist)
        
        self.forage(dt)
            
    def forage(self,amt):
        veg = self.map.fetch_scent('Vegetation').data[ self.pos[0], self.pos[1] ]
            
    def walk(self,dx,dy):
        self.pos[0] += int(dx)
        self.pos[1] += int(dy)
                
    def forage(self,dt):
        own = self.map.ownership.data[self.x,self.y]
        if own == 0 or own == int(util.short_id(self.id), 16): 
            #we can forage this spot
            pass

    def image(self):
        if self.myimage is not None: return self.myimage
        self.myimage = GoblinImage(unit=self)
        return self.myimage
        
    def update(self,dt):
        self.map.deposit_scent('Goblin',self.pos,dt)
        self.map.deposit_scent('Wealth',self.pos,max(0,self.wealth)*dt/3600.)
        self.wander(dt)
        self.myimage.refresh()
