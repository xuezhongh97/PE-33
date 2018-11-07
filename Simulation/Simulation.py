# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 16:42:27 2018

@author: Paul
"""

from tkinter import *
from random import *
import numpy as np
from Entities import *
from Zone import *

# The main window, with link to every other windows
        
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
        self.zone_frame.grid(row=0,column=0)
        
        # Frame 2 : buildings
        self.building_frame = Frame(self)
        r,c=0,0
        Label(self.building_frame,text='Paramètre des bâtiments',bg='gray70').grid(row=r,column=c,columnspan=2)
        r+=1
        Button(self.building_frame,text='gérer architecture',command=self.build).grid(row=r,column=c)
        self.building_frame.grid(row=0,column=1,sticky=N)
        
        # Run button
        Button(self,text="Demarer (Entrer)",command=self.run,height=4,width=20).grid(row=1,column=4)
    
    def build(self):   # Open a building zone to manage buildings and walls
        e=self.ppc
        w,h=e*(int(self.width_entry.get())//e),e*(int(self.height_entry.get())//e)
        
        if self.entities == None:                  # The first time that a building zone is opened, self.entities is initialized with the parameters of the zone
            self.entities = Entities (self,e,w,h)
            
        Z = Building_zone(self,w,h)
        Z.lift()
        Z.focus_force()
    
    def run(self):     # Open a viewing zone and launch the simulation
        return None
        
    def leave(self,event):
        self.destroy()