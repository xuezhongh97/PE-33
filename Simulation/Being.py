# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:38:58 2018

@author: Nicolas
"""

from tkinter import *
from Entities import *
import numpy as np

class Being:
    def __init__(self,master,pixposition,cell,speed):
        self.master=master
        self.pixposition=pixposition      # (x,y) for position in pixels
        self.cell=cell                  # The cell the being is in
        self.speed=speed                # (vr,vteta) vr is the norm and vteta the angle of the speed
    
    def move(self,t):
        self.pixposition[0]+=t*self.speed[0]*np.cos(self.speed[1])                  #new position of the being
        self.pixposition[1]+=t*self.speed[0]*np.sin(self.speed[1])
        self.cell=self.master.which_cell(self.pixposition[0],self.pixposition[1])
        
class Zombie(Being):
    def __init__(self,master,pixposition,case,speed,lifespan):
        Being.__init__(self,master,pixposition,case,speed)
        self.lifespan=lifespan
        
class Human(Being):
    def __init__(self,master,pixposition,case,speed):
        Being.__init__(self,master,pixposition,case,speed)
