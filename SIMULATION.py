# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 16:42:27 2018

@author: Paul
"""

from tkinter import *
from random import *
import numpy as np

class Case:
    def __init__(self,master,x,y,nx,ny):
        self.master=master
        self.center=[x,y]     # Position in pixels of the center
        self.n=[nx,ny]       # Position in the grid

class Viewing_zone:
    def __init__(self,master,n,size):     #n is the number of cases per row/column, and size the number of pixels of width/height of the viewing zone
        self.master=master
        # Cases initialisation
        self.grid=[]
        c=size/n       # number of pixels of length of a case (suppose that size is a multiple of n)
        x,y=c/2,c/2        # will be the centers of the cases
        for j in range (n):
            L=[]
            for i in range (n):
                L.append(Case(self,x,y,i,j))
                x+=c
            self.grid.append(L)
            y+=c

class Entities:
    def __init__(self,master):
        self.master=master
        self.buildings=[]
        self.humans=[]
        self.zombies=[]
        
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

class Building:
    def __init__(self,master,cases):
        self.master=master
        self.walls=[]
        for c in cases:
            self.walls.append(wall(self,c))
            
class Wall:
    def __init__(self,master,case):
        self.master=master
        self.case=case
        
class Simulation:
    def __init__(self):
        self.entites= Entities(self)
        self.viewing_zone= Viewing_zone(self,80,800)