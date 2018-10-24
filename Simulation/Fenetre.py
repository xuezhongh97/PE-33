# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:41:44 2018

@author: Nicolas
"""
from tkinter import *

class Viewing_zone:
    def __init__(self,master):     #n is the number of cells per row/column, and size the number of pixels of width/height of the viewing zone
        self.master=master
        
class Building_zone(Toplevel):
    def __init__(self,master,w,h):
        Toplevel.__init__(self)
        self.master = master
        self.canvas = Canvas(self,width=w,height=h)
        self.canvas.grid()
        # Binding
        self.canvas.bind('<B1-Motion>',self.clic)  # Allow to add walls by maintaining clic
        self.canvas.bind('<Button-1>',self.clic)   # Allow to add a wall with clic
        self.bind('<Escape>',self.leave)
        for wall in self.master.entities.walls:    # Plot walls that are already saved when oppening a building zone
            wall.plot(self.canvas)
        
    def clic(self,event):
        x,y=event.x,event.y
        (nx,ny)=self.master.entities.which_cell(x,y)      # les indices de la case sur laquelle on a cliqué
        wall=Wall(self.master,self.master.entities.grid[nx][ny])
        self.master.entities.walls.append(wall)
        self.master.entities.grid[nx][ny].set_wall(wall)
        wall.plot(self.canvas)
        
    def leave(self,event):
        self.destroy()
