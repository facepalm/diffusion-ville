import numpy as np
from scipy.stats import wald
import random

import globalvars
import systempanel
import util
import planet
import structures.ark as ark
import structures.structure as structure
import hohmann

class Universe(object):    
    def __init__(self):
        self.generate_system()
        
    def generate_system(self,system_type='Generic'):            
    
        self.system_distribution = util.getWackyDist(total_mass = 1E29, objects = 20, wacky_facty = 0.5)
                            
        primary_star_mass = wald.rvs(loc=0.2, scale=1.5, size=1)[0]
        
        #self.system_distribution = self.system_distribution[self.system_distribution != primary_star_mass]
        
        self.primary = planet.Star(solar_masses=primary_star_mass)
        
        print self.primary.info()
        
        num_orbits = np.random.randint(8,18)
        orbits = [pow(10,1.5*x)- 0.6 for x in np.random.random(num_orbits)]
        #np.random.shuffle( orbits )
        #orbits = orbits[ orbits != 2 ]
        orbit_mass = np.random.choice(self.system_distribution,size=num_orbits,replace=False)
        
        self.planets = []
        
        for i in range(num_orbits):
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
        globalvars.root.screen_manager.current = self.primary.view.name

    def update(self,dt):
        for obj in globalvars.ids.values():
            if hasattr(obj,'update'):
                obj.update(dt)
                
    def add_exploration(self,amt=0.0001,limit=0.1):
        for obj in globalvars.ids.values():
            if isinstance(obj,planet.Planet) or isinstance(obj,planet.Star):
                obj.add_exploration(amt,limit)
        
