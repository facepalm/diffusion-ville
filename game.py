import numpy as np
from scipy.stats import wald
import random

import globalvars
import util

import maps

import cv2


class Universe(object):    
    def __init__(self):
        self.generate_world()
        
    def generate_world(self,world_type='Generic'):            
            
        self.maptype = random.choice(['FOREST','GRASSLAND','VALLEY'])

        if self.maptype == 'FOREST':
            self.game_map = maps.Map(size=[300,300])
            self.game_map.vegetation.randomize('pareto',4)
            self.game_map.elevation.randomize('pareto',5)
            self.game_map.elevation.diffuse(10)
        elif self.maptype == 'GRASSLAND':
            self.game_map = maps.Map(size=[300,300])
            self.game_map.vegetation.randomize('pareto',5)
            self.game_map.elevation.randomize('pareto',5)
            self.game_map.elevation.diffuse(10)
        else: #VALLEY
            self.game_map = maps.Map(size=[500,200])
            self.game_map.vegetation.randomize('pareto',2)
            self.game_map.elevation.randomize('pareto',5)
            for i in range(0,15):
                p1 = [random.randint(0,199),random.randint(20,480)]
                p2 = [random.randint(0,199),random.randint(20,480)]
                p1[0] *= pow(p1[1]/500.,3)
                p2[0] = 199 - p2[0]*pow(p2[1]/500.,3)
                print p1, p2
                self.game_map.elevation.data[p1[1],p1[0]] = random.randint(10000,20000)*p1[1]/500.
                self.game_map.elevation.data[p2[1],p2[0]] = random.randint(10000,20000)*p2[1]/500.     
            for i in range(50): self.game_map.elevation.diffuse(5)
            self.game_map.elevation.data *= 100/self.game_map.elevation.data.max()
            
        treeline = 20    
        self.game_map.vegetation.bloom(treeline-self.game_map.elevation.data)   
            
        mapscreen = maps.MapScreen()
        mapscreen.name = 'Home Map'
        mapscreen.ids['mapscroll'].add_widget(self.game_map)
            
        globalvars.root.screen_manager.add_widget(mapscreen)      
        globalvars.root.screen_manager.current = mapscreen.name
            
        #imdata = self.game_map.vegetation.data.copy()
        #print imdata
        #m = max(imdata.ravel())
        #imdata = np.divide(imdata,m)
        
        #cv2.imshow('rawfield', imdata)
        #cv2.waitKey(100)   
        
        #self.system_distribution = util.getWackyDist(total_mass = 1E29, objects = 20, wacky_facty = 0.5)
                            
        #primary_star_mass = wald.rvs(loc=0.2, scale=1.5, size=1)[0]
        
        #self.system_distribution = self.system_distribution[self.system_distribution != primary_star_mass]
        
        #self.primary = planet.Star(solar_masses=primary_star_mass)
        
        #print self.primary.info()
        
        #num_orbits = np.random.randint(8,18)
        #orbits = [pow(10,1.5*x)- 0.6 for x in np.random.random(num_orbits)]
        #np.random.shuffle( orbits )
        #orbits = orbits[ orbits != 2 ]
        #orbit_mass = np.random.choice(self.system_distribution,size=num_orbits,replace=False)
        
        #self.planets = []
        
        '''for i in range(num_orbits):
            mass = orbit_mass[i]
            print mass, orbits[i]
                
            #initialize planet, extend list (might be a list of asteroids instead)    
            newp = planet.generate_planet(mass,self.primary,orbits[i])
            for p in newp:
                globalvars.root.screen_manager.add_widget(p.view)
                print p.view.name, globalvars.root.screen_manager.children
            self.planets.extend(newp)
            
        #habitable zone world        
        newp = planet.generate_planet(random.random()*9E24 + 1E24,self.primary,self.primary.random_habitable_orbit())
        for p in newp:
            globalvars.root.screen_manager.add_widget(p.view)
        self.planets.extend(newp)  
        
        #hohmann.calculate_hohmann(random.choice(self.planets),random.choice(self.planets))
        #hohmann.transfer_breakdown(random.choice(random.choice(self.planets).sites),random.choice(random.choice(self.planets).sites))
        #quit()
        
        #instantiate Ark
        theArk = ark.Ark(site=newp[0].sites[0])
        theArk.build(free=True)  
        newp[0].sites[0].resources.add('antimatter',1000)
        newp[0].sites[0].resources.add('rocket engines',100)
        newp[0].sites[0].resources.add('rocket fuel',1000)
        
        t = structure.RTG(site=newp[0].sites[0])
        t.build(free=True)
        
        
        reg = structure.PlaceholderRegolithMiner(site=newp[0].sites[0])
        reg.build(free=True)  

        
        #print theArk.composition
        self.primary.view.system_view.update()
        globalvars.root.screen_manager.add_widget(self.primary.view)      
        globalvars.root.screen_manager.current = self.primary.view.name'''

    def update(self,dt):
        for obj in globalvars.ids.values():
            if hasattr(obj,'update'):
                obj.update(dt)
                
    def add_exploration(self,amt=0.0001,limit=0.1):
        for obj in globalvars.ids.values():
            if isinstance(obj,planet.Planet) or isinstance(obj,planet.Star):
                obj.add_exploration(amt,limit)
        
