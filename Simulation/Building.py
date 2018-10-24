# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:41:01 2018

@author: Nicolas
"""
from tkinter import *

class Cell:
    def __init__(self,master,x,y,nx,ny,ppc,floors):
        self.master=master
        self.center=[x,y]     # Position in pixels of the center
        self.n=[nx,ny]       # Position in the grid
        self.ppc=ppc
        self.floors=floors
        self.content=None
        
    def set_wall(self,wall):
        self.content=wall

class Building:
    def __init__(self,master,cells):
        self.master=master
        self.walls=[]
        for c in cells:
            self.walls.append(Wall(self,c))
            
class Wall:
    def __init__(self,master,cell):
        self.master=master
        self.cell=cell
        
    def plot(self,zone):
        [xc,yc],e=self.cell.center,self.cell.ppc
        zone.create_rectangle(xc-e//2,yc-e//2,xc+e//2,yc+e//2,fill='black')