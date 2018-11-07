# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:41:44 2018

@author: Nicolas
"""
from tkinter import *
from Building import *

# Viewing zone is the window where we see the simulation, no input from the user, just the simulation's run

class Viewing_zone:
    def __init__(self,master):     #n is the number of cells per row/column, and size the number of pixels of width/height of the viewing zone
        self.master=master
        
# Building zone is the window where we manage building's configuration
        
class Building_zone(Toplevel):
    def __init__(self,master,w,h):
        Toplevel.__init__(self)
        self.master = master
        
        # Visual zone
        self.canvas = Canvas(self,width=w,height=h,bg='gray50')
        self.canvas.grid(row=0,column=0,rowspan=6)
        for wall in self.master.entities.walls:    # Plot walls that are already saved when oppening a building zone
            wall.plot(self.canvas)
            
        # Settings zone
        self.frame_1 = Frame(self)
        r,c=0,0    # row and column of widgets in frame_1
        Button(self.frame_1,text='Nettoyer',command=self.clear).grid(row=r,column=c)
        r+=1
        self.coor_label = Label(self.frame_1,text='coordonnées :\n(0,0)')
        self.coor_label.grid(row=r,column=c,rowspan=2)
        Button(self.frame_1,text='Creer un mur au clic',command=self.setclic_wall)
        self.frame_1.grid(row=0,column=1,sticky=N)
        
        # New building zone : where we can create a new building
        self.frame_2 = Frame(self)
        Label(self.frame_2,text='--------------------------').grid(row=0,column=0,columnspan=2)
        Label(self.frame_2,text='Bâtiments rectangulaires').grid(row=1,column=0,columnspan=2)
        Label(self.frame_2,text='largeur :').grid(row=2,column=0)
        Label(self.frame_2,text='hauteur :').grid(row=3,column=0)
        Button(self.frame_2,text='Creer un bâtiment au clic',command=self.setclic_building)
        self.width_entry = Entry(self.frame_2)
        self.height_entry = Entry(self.frame_2)
        self.width_entry.grid(row=2,column=1)
        self.height_entry.grid(row=3,column=1)
        self.frame_2.grid(row=1,column=1,sticky=N)
        
        # Binding
        self.canvas.bind('<Button-3>',self.coordinates)  # Allow to print the coordinates of the point that is right-clicked
        self.bind('<Escape>',self.leave)
        
    def clic_wall(self,event):   # called to create a wall
        x,y=event.x,event.y
        (nx,ny)=self.master.entities.which_cell(x,y)      # The indices of the case that were clicked on
        self.master.entities.walls.append((nx,ny))
        self.master.entities.grid[nx][ny].set_wall()
        self.master.entities.grid[nx][ny].plot(self.canvas)
        
    def clic_building(self,event):    # called to create a building
        w,h=int(self.width_entry.get()),int(self.height_entry.get())
        (nx,ny)=self.master.entities.which_cell(event.x,event.y)
        no=(nx-w//2,ny-h//2)     # top left cell
        se=(no[0]+w-1,no[1]+h-1)     # bottom right cell
        walls=[(nx + k,ny) for k in range(w)]+[(nx+k,ny+h-1) for k in range(w)]+[(nx,ny+k) for k in range(1,h-1)]+[(nx+w-1,ny+k) for k in range(1,h-1)]
        
        # A terminer
        
    def coordinates(self,event):
        x,y=event.x,event.y
        (nx,ny)=self.master.entities.which_cell(x,y)
        self.coor_label.config(text='coordonnées :\n('+str(nx)+','+str(ny)+')')
        
    def setclic_building(self):
        self.canvas.bind('<Button-1>',self.clic_building)   # Allow to add a wall with clic
        
    def setclic_wall(self):
        self.canvas.bind('<B1-Motion>',self.clic_wall)  # Allow to add walls by maintaining clic
        self.canvas.bind('<Button-1>',self.clic_wall)   # Allow to add a wall with clic
        
    def clear(self):
        self.master.entities.reset_grid()
        self.master.entities.reset_walls()
        self.canvas.delete('all')
        
    def leave(self,event):
        self.destroy()