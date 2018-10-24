# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:38:58 2018

@author: Nicolas
"""

from tkinter import *

class Being:
    def __init__(self,master,pixposition,case,speed):
        self.master=master
        self.pixposition=pixposition      # (x,y) for position in pixels
        self.case=case                   # The case the being is in
        self.speed=speed                # (vr,vteta) vr is the norm and vteta the angle of the speed
        
class Zombie(Being):
    def __init__(self,master,pixposition,case,speed,lifespan):
        Being.__init__(self,master,pixposition,case,speed)
        self.lifespan=lifespan
        
class Human(Being):
    def __init__(self,master,pixposition,case,speed):
        Being.__init__(self,master,pixposition,case,speed)
