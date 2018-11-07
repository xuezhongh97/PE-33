# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:42:18 2018

@author: Nicolas
"""

from tkinter import *
from Building import *

class Entities:
    def __init__(self,master,e,w,h):
        self.master=master
        self.walls=[]      # list of cells' indices (nx,ny)
        self.buildings=[]
        self.humans=[]
        self.zombies=[]
        self.grid=[]      # list of all the cells
        self.size=[w,h]
        self.ppc=e       # Pixels per case : number of pixels of length of a case
        self.reset_grid()
    
    def which_cell(self,x,y):                             # When given (x,y) coordinates, return the indices of the associated cell
                                                          # Complexity 0(1)
        if x>self.size[0] or y>self.size[1] or x<0 or y<0:
            return None
        return (x//self.ppc,y//self.ppc)
    
    def reset_grid(self):
        self.grid=[]
        x,y,nx,ny=self.ppc//2,self.ppc//2,self.size[0]//self.ppc,self.size[1]//self.ppc
        for i in range (nx):
            L,y=[],self.ppc//2
            for j in range (ny):
                L.append(Cell(self,x,y,i,j,self.ppc,1))
                y+=self.ppc
            self.grid.append(L)
            x+=self.ppc
    
    def reset_walls(self):
        self.walls=[]