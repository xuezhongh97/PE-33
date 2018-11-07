# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:41:01 2018

@author: Nicolas
"""
from tkinter import *

class Cell:
    def __init__(self,master,x,y,nx,ny,floors):
        self.master=master     # the entities object
        self.center=[x,y]     # Position in pixels of the center
        self.n=[nx,ny]       # Position in the grid
        self.floors=floors
        self.content=None
        
    def set_wall(self):
        self.content='w'
    
    def plot(self,zone):                    #permet d'afficher les batiments
        [xc,yc],e=self.center,self.master.ppc
        zone.create_rectangle(xc-e//2,yc-e//2,xc+e//2,yc+e//2,fill='black')

class Building:
    def __init__(self,master):
        self.master=master
        self.walls=[]     # list of cells
