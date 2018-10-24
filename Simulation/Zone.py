# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:41:44 2018

@author: Nicolas
"""
from tkinter import *
from Building import *

class Viewing_zone:
    def __init__(self,master):     #n is the number of cells per row/column, and size the number of pixels of width/height of the viewing zone
        self.master=master
        
class Building_zone(Toplevel):
    def __init__(self,master,w,h):
        Toplevel.__init__(self)
        self.master = master
        
        # Visual zone
        self.canvas = Canvas(self,width=w,height=h)
        self.canvas.grid(row=0,column=0)
        for wall in self.master.entities.walls:    # Plot walls that are already saved when oppening a building zone
            wall.plot(self.canvas)
            
        # Settings zone
        self.frame_1 = Frame(self)
        r,c=0,0    # row and column of widgets in frame_1
        Button(self.frame_1,text='Nettoyer',command=self.clear).grid(row=r,column=c)
        r+=1
        self.coor_label = Label(self.frame_1,text='coordonnées :\n(0,0)')
        self.coor_label.grid(row=r,column=c,rowspan=2)
        self.frame_1.grid(row=0,column=1,sticky=N)
        
        # Binding
        self.canvas.bind('<B1-Motion>',self.clic)  # Allow to add walls by maintaining clic
        self.canvas.bind('<Button-1>',self.clic)   # Allow to add a wall with clic
        self.canvas.bind('<Button-3>',self.coordinates)
        self.bind('<Escape>',self.leave)
        
    def clic(self,event):
        x,y=event.x,event.y
        (nx,ny)=self.master.entities.which_cell(x,y)      # les indices de la case sur laquelle on a cliqué
        wall=Wall(self.master,self.master.entities.grid[nx][ny])
        self.master.entities.walls.append(wall)
        self.master.entities.grid[nx][ny].set_wall(wall)
        wall.plot(self.canvas)
        
    def coordinates(self,event):
        x,y=event.x,event.y
        (nx,ny)=self.master.entities.which_cell(x,y)
        self.coor_label.config(text='coordonnées :\n('+str(nx)+','+str(ny)+')')
        
    def clear(self):
        self.master.entities.reset_grid()
        self.master.entities.reset_walls()
        self.canvas.delete('all')
        
    def leave(self,event):
        self.destroy()
