# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:38:58 2018

@author: Nicolas
"""

from tkinter import *
from Entities import *
import numpy as np
import time

class Being:
    def __init__(self,master,pixposition,cell,speed,vision,hearing,strength,agility,mental):
        self.master=master
        self.pixposition=pixposition      # (x,y) for position in pixels
        self.cell=cell                  # The cell the being is in
        self.speed=speed                # (vr,vteta) vr is the norm and vteta the angle of the speed
        self.vision=vision              #vision distance
        self.hearing=hearing                    #hearing threshold
        self.strength=strength              #physical trait (don't change)
        self.agilty=agility                 #agility trait (don't change)
        self.mental=mental                  #mental trait (don't change)
    
    def move(self,t):
        self.pixposition[0]+=t*self.speed[0]*np.cos(self.speed[1])                  #new position of the being
        self.pixposition[1]+=t*self.speed[0]*np.sin(self.speed[1])
        self.cell=self.master.which_cell(self.pixposition[0],self.pixposition[1])
        
class Zombie(Being):
    def __init__(self,master,pixposition,cell,speed):
        zombie_vision=
        zombie_hearing=
        zombie_strength=
        zombie_agility=
        zombie_mental=
        zombie_lifespan=
        Being.__init__(self,master,pixposition,cell,speed,zombie_vision,zombie_hearing,zombie_strength,zombie_agility,zombie_mental)
        self.lifespan=zombie_lifespan
        
class Human(Being):
    def __init__(self,master,pixposition,cell,speed,vision,hearing,strength,agility,mental,morality,survival,hunger,energy,stress,stamina):
        Being.__init__(self,master,pixposition,cell,speed,vision,hearing,strength,agility,mental)
        self.morality=morality              #define the morality of the human
        self.survival=survival              #define the type of survival (hide,flee,fight,...)
        self.hunger=hunger                  #hunger (decrease by time) 0=death
        self.energy=energy                  #energy (decrease by time) 0=death
        self.stress=stress                  #quantity of stress (determine the quality of the decisions)
        self.stamina=stamina                #stamina (decrease when running) 0=no more running
        self.knowing=False                  #knowing the zombie invasion
    
    def zombification(self):
        time.sleep(zombie_incubationtime*dt)                #waiting for the human to turn into a zombie
        self.master.humans.remove(self)              #removing the entity from class human
        self.master.zombies.add(Zombie(self.master,self.pixposition,self.cell,0))             #creating a new zombie
    
    def eaten(self):
        self.master.humans.remove(self)