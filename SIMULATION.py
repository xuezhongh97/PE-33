# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 16:42:27 2018

@author: Paul
"""

from tkinter import *
from random import *
import numpy as np

class Case:
    def __init__(self,master,x,y,nx,ny,ppc,floors):
        self.master=master
        self.center=[x,y]     # Position in pixels of the center
        self.n=[nx,ny]       # Position in the grid
        self.ppc=ppc
        self.floors=floors
        self.content=None
        
    def set_wall(self,wall):
        self.content=wall

class Viewing_zone:
    def __init__(self,master):     #n is the number of cases per row/column, and size the number of pixels of width/height of the viewing zone
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
        (nx,ny)=self.master.entities.which_case(x,y)      # les indices de la case sur laquelle on a cliqué
        wall=Wall(self.master,self.master.entities.grid[nx][ny])
        self.master.entities.walls.append(wall)
        self.master.entities.grid[nx][ny].set_wall(wall)
        wall.plot(self.canvas)
        
    def leave(self,event):
        self.destroy()

class Entities:
    def __init__(self,master,e,w,h):
        self.master=master
        self.walls=[]
        self.humans=[]
        self.zombies=[]
        self.grid=[]
        self.size=[w,h]
        self.ppc=e       # Pixels per case : number of pixels of length of a case
        x,y,nx,ny=self.ppc//2,self.ppc//2,w//e,h//e       # will be the centers of the cases
        for i in range (nx):
            L,y=[],self.ppc//2
            for j in range (ny):
                L.append(Case(self,x,y,i,j,e,1))
                y+=self.ppc
            self.grid.append(L)
            x+=self.ppc
    
    def which_case(self,x,y):
        if x>self.size[0] or y>self.size[1] or x<0 or y<0:
            return None
        return (x//self.ppc,y//self.ppc)
        
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
            self.walls.append(Wall(self,c))
            
class Wall:
    def __init__(self,master,case):
        self.master=master
        self.case=case
    def plot(self,zone):
        [xc,yc],e=self.case.center,self.case.ppc
        zone.create_rectangle(xc-e//2,yc-e//2,xc+e//2,yc+e//2,fill='black')
        
class Simulation(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry('1000x800')
        self.config(bg='gray70')
        self.bind('<Escape>',self.leave)
        
        # Données
        self.entities = None
        self.ppc = 10
        
        # Paramètres
        # Frame 1 : Zone
        self.zone_frame = Frame(self,bg='gray70')
        r=0
        Label(self.zone_frame,text='Paramètre de la zone',bg='gray70',width=30).grid(row=r,column=0,columnspan=2)
        r+=1
        Label(self.zone_frame,text='largeur :',bg='gray70').grid(row=r,column=0)
        self.width_entry= Entry(self.zone_frame,bg='gray80',width=8)
        self.width_entry.insert(END,'1500')
        self.width_entry.grid(row=r,column=1)
        r+=1
        Label(self.zone_frame,text='hauteur :',bg='gray70').grid(row=r,column=0)
        self.height_entry= Entry(self.zone_frame,bg='gray80',width=8)
        self.height_entry.insert(END,'800')
        self.height_entry.grid(row=r,column=1)
        r+=1
        Button(self.zone_frame,text='gérer architecture',command=self.build).grid(row=r,column=0)
        
        self.zone_frame.grid(row=0,column=0)
        # Frame 2 : buildings
        self.building_frame = Frame(self)
        r,c=0,0
        Label(self.building_frame,text='Paramètre des bâtiments',bg='gray70').grid(row=r,column=c,columnspan=2)
        self.building_frame.grid(row=0,column=1)
        
        Button(self,text="Demarer (Entrer)",command=self.run,height=4,width=20).grid(row=1,column=4)
    
    def build(self):
        e=self.ppc
        w,h=e*(int(self.width_entry.get())//e),e*(int(self.height_entry.get())//e)
        self.entities = Entities (self,e,w,h)
        Z = Building_zone(self,w,h)
        Z.lift()
        Z.focus_force()
    
    def run(self):
        return None
        
    def leave(self,event):
        self.destroy()

simulation=Simulation()
simulation.focus_force()
simulation.lift()
simulation.mainloop()