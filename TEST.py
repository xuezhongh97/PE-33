# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 14:13:09 2018

@author: Nicolas
"""

from tkinter import *
from numpy import *
from random import *

fen_size=[800,800]
epaisseur=3
irate=0.3

def isin(a,b,c):
    return (b[0]<=a[0]<=c[0] or c[0]<=a[0]<=b[0]) and (b[1]<=a[1]<=c[1] or c[1]<=a[1]<=b[1])

def dist(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5
def norme(p):
    return (p[0]**2+p[1]**2)**0.5

class entree:
    def __init__(self,bati,pos):
        self.bati=bati    # Le batiment sur lequel se trouve l'entrée
        self.position=pos     # Nord,Est,Sud, ou Ouest

class batiment:
    def __init__(self,master,c1,c2,nbati):
        self.master=master
        self.c1=c1   #coin haut gauche
        self.c2=c2    #coin bas droite
        self.panique=False
        self.any_hum=False
        self.rect=self.master.can.create_rectangle(c1[0],c1[1],c2[0],c2[1],outline='black',width=epaisseur)
        self.label=self.master.can.create_text(c1[0]+epaisseur+5,c1[1]+epaisseur+10,text=str(nbati))
        self.entrees=[]
    def isin(self,p):
        return isin(p,self.c1,self.c2)
    def test(self,p1,p2):
        c1,c2=self.c1,self.c2
        c3,c4,p3,p4=[c1[0],c2[1]],[c2[0],c1[1]],[p1[0],p2[1]],[p2[0],p1[1]]
        return (isin(p1,c1,c2) or isin(p2,c1,c2) or isin(p3,c1,c2) or isin(p4,c1,c2) or isin(c1,p1,p2) or isin(c2,p1,p2) or isin(c3,p1,p2) or isin(c4,p1,p2))
    def test_panique(self):
        panique=False
        for z in self.master.infec:
            if z.localisation == self:
                panique=True
        self.panique=panique

class personne:
    def __init__(self,master,pos,v,loca,ide):
        self.master=master
        self.pos=pos
        self.localisation=loca
        self.localisation.any_hum=True
        self.vit=[v,2*pi*random()]
        self.id=ide
    def move_random(self,t):
        if random()<=0.5*t:
            self.vit[1]=2*pi*random()
        dx,dy=self.vit[0]*0.3*cos(self.vit[1])*t,self.vit[0]*0.3*sin(self.vit[1])*t
        [x,y]=self.pos
        c1,c2=self.localisation.c1,self.localisation.c2
        if x+dx<c1[0]+epaisseur:
            if randint(0,1)==1:
                self.vit[1]=random()*pi/2
            else:
                self.vit[1]=3*pi/2+random()*pi/2
            dx=0
        elif x+dx>c2[0]-epaisseur:
            self.vit[1]=pi/2+random()*pi
            dx=0
        else:
            x=x+dx
        if y+dy<c1[1]+epaisseur:
            self.vit[1]=random()*pi
            dy=0
        elif y+dy>c2[1]-epaisseur:
            self.vit[1]=pi+random()*pi
            dy=0
        else:
            y=y+dy
        self.pos=[x,y]
        self.master.can.move(self.point,dx,dy)
        
class humain(personne):
    def __init__(self,master,pos,v,loca,ide):
        personne.__init__(self,master,pos,v,loca,ide)
        self.point=master.can.create_oval(pos[0]-epaisseur,pos[1]-epaisseur,pos[0]+epaisseur,pos[1]+epaisseur,fill='green')     #id du point
        self.alive=True
    def move(self,t):
        if self.localisation.panique:
            dx,dy=self.vit[0]*cos(self.vit[1])*t,self.vit[0]*sin(self.vit[1])*t
            [x,y]=self.pos
            c1,c2=self.localisation.c1,self.localisation.c2
            if x+dx<c1[0]+epaisseur:
                if randint(0,1)==1:
                    self.vit[1]=random()*pi/2
                else:
                    self.vit[1]=3*pi/2+random()*pi/2
                dx=0
            elif x+dx>c2[0]-epaisseur:
                self.vit[1]=pi/2+random()*pi
                dx=0
            else:
                x=x+dx
            if y+dy<c1[1]+epaisseur:
                self.vit[1]=random()*pi
                dy=0
            elif y+dy>c2[1]-epaisseur:
                self.vit[1]=pi+random()*pi
                dy=0
            else:
                y=y+dy
            self.pos=[x,y]
            self.master.can.move(self.point,dx,dy)
        else:
            self.move_random(t)
            
    def contaminer(self,killer):
        self.master.retire(self.id,'h')
        self.alive=False
        if random()<self.master.irate:
            self.master.infec.append(zombie(self.master,self.pos,killer.vit[0],self.localisation,self.master.id,killer.dureeVieMax))
            self.master.id+=1
        self.master.can.delete(self.point)
        
class zombie(personne):
    def __init__(self,master,pos,v,loca,ide,dureeVie):
        personne.__init__(self,master,pos,v,loca,ide)
        self.localisation.panique=True
        self.target=None
        self.actif=True
        self.point=master.can.create_oval(pos[0]-epaisseur,pos[1]-epaisseur,pos[0]+epaisseur,pos[1]+epaisseur,fill='red')      #id du point
        self.dureeVie = dureeVie
        self.dureeVieMax = dureeVie
    def move(self,t):
        self.dureeVie-=t
        if self.dureeVie<0:
            self.kill()
        if self.actif:
            if self.target == None:
                L=[]
                for h in self.master.pop:
                    if h.localisation == self.localisation:
                        L.append(h)
                if len(L)>0:
                    self.target = L[randint(0,len(L)-1)]
                else:
                    self.actif=False
            else:
                if self.target.alive == False:
                    self.target = None
                elif dist(self.pos,self.target.pos)<2*epaisseur:
                    self.target.contaminer(self)
                    self.target = None
                else:
                    dl=[self.target.pos[0]-self.pos[0],self.target.pos[1]-self.pos[1]]
                    self.vit[1]=2*arctan(dl[1]/(norme(dl)+dl[0]))
                    dx,dy=self.vit[0]*cos(self.vit[1])*t,self.vit[0]*sin(self.vit[1])*t
                    self.pos=[self.pos[0]+dx,self.pos[1]+dy]
                    self.master.can.move(self.point,dx,dy)
        else:
            if self.localisation.any_hum:
                self.actif=True
            self.move_random(t)
                    
    def kill(self):
        self.master.retire(self.id,'z')
        self.master.can.delete(self.point)
        self.localisation.test_panique()

class fenetre(Tk):
    def __init__(self):
        Tk.__init__(self)
        #donnees
        self.bati_sizex=350
        self.bati_sizey=350
        self.t=0.05
        self.id=0
        self.irate=1
        self.dureeVie=20
        self.n_hspawn='*'
        self.n_zspawn='*'
        self.v_zom=10
        self.v_hum=10
        #espace
        self.can = Canvas(self,height=fen_size[0],width=fen_size[1],bg='gray65')
        self.can.grid(row=0,column=0,rowspan=5)
        self.archi=[]           # future liste des batiments
        self.pop=[]           # future liste des humains
        self.infec=[]         # future liste des zombies
        self.can.bind('<Button-1>',self.ajout_batiment)
        
        #contrôle zone 1 : batiments
        self.fbati = Frame(self)
        row=0
        Label(self.fbati,text='------------------ Bâtiments -----------------').grid(row=row,column=0,columnspan=3)
        row+=1
        Label(self.fbati,text='Taille des bâtiments :').grid(row=row,column=0,columnspan=2)
        row+=1
        Label(self.fbati,text='largeur :').grid(row=row,column=0)
        self.entry_sizex = Entry(self.fbati,width=5)
        self.entry_sizex.grid(row=row,column=1)
        row+=1
        Label(self.fbati,text='hauteur :').grid(row=row,column=0)
        self.entry_sizey = Entry(self.fbati,width=5)
        self.entry_sizey.grid(row=row,column=1)
        row+=1
        Button(self.fbati,text='valider',command=self.modif_size).grid(row=row,column=0)
        row+=1
        self.label_size = Label(self.fbati,text='Actuellement :\n largeur '+str(self.bati_sizex)+'\n hauteur '+str(self.bati_sizey))
        self.label_size.grid(row=row,column=0,columnspan=3,rowspan=3)
        self.fbati.grid(row=0,column=1,sticky=NE)
        
        #contrôle zone 2 : humains
        #zone 2.1
        self.fhum = Frame(self)
        row=0
        Label(self.fhum,text='------------------ Humains -----------------').grid(row=row,column=0,columnspan=3)
        row+=1
        Label(self.fhum,text='Nombre à spawn :').grid(row=row,column=0)
        self.entry_hum = Entry(self.fhum,width=5)
        self.entry_hum.insert(END,'10')
        self.entry_hum.grid(row=row,column=1)
        Button(self.fhum,text='spawn',command=self.hspawn).grid(row=row,column=2)
        row+=1
        Label(self.fhum,text='-------------------------------').grid(row=row,column=0,columnspan=3)
        row+=1
        Label(self.fhum,text='Spawn dans (* = any) :').grid(row=row,column=0)
        self.entry_hspawn = Entry(self.fhum,width=5)
        self.entry_hspawn.grid(row=row,column=1)
        Button(self.fhum,text='valider',command=self.set_hspawn).grid(row=row,column=2)
        row+=1
        self.hspawn_label = Label(self.fhum,text='Actuellement : '+self.n_hspawn)
        self.hspawn_label.grid(row=row,column=0,columnspan=3)
        row+=1
        Label(self.fhum,text='-------------------------------').grid(row=row,column=0,columnspan=3)
        row+=1
        #zone 2.2
        Label(self.fhum,text='Vitesse : ').grid(row=row,column=0)
        self.entry_v_hum = Entry(self.fhum,width=5)
        self.entry_v_hum.grid(row=row,column=1)
        Button(self.fhum,text='Valider',command=self.set_vhum).grid(row=row,column=2)
        row+=1
        self.vhum_label = Label(self.fhum,text='Actuellement : '+str(self.v_hum))
        self.vhum_label.grid(row=row,column=0,columnspan=3)
        self.fhum.grid(row=0,column=3,rowspan=2,sticky=N)
        
        #contrôle zone 3 : zombies
        #zone 3.1
        self.fzom = Frame(self)
        row=0
        Label(self.fzom,text='------------------ Zombies -----------------').grid(row=row,column=0,columnspan=3)
        row+=1
        Label(self.fzom,text='Nombre à spawn :').grid(row=row,column=0)
        self.entry_zom = Entry(self.fzom,width=5)
        self.entry_zom.insert(END,'1')
        self.entry_zom.grid(row=row,column=1)
        Button(self.fzom,text='spawn',command=self.zspawn).grid(row=row,column=2)
        row+=1
        Label(self.fzom,text='-------------------------------').grid(row=row,column=0,columnspan=3)
        row+=1
        Label(self.fzom,text='Spawn dans (* = any) :').grid(row=row,column=0)
        self.entry_zspawn = Entry(self.fzom,width=5)
        self.entry_zspawn.grid(row=row,column=1)
        Button(self.fzom,text='valider',command=self.set_zspawn).grid(row=row,column=2)
        row+=1
        self.zspawn_label = Label(self.fzom,text='Actuellement : '+self.n_zspawn)
        self.zspawn_label.grid(row=row,column=0,columnspan=3)
        row+=1
        Label(self.fzom,text='-------------------------------').grid(row=row,column=0,columnspan=3)
        row+=1
        #zone 3.2
        Label(self.fzom,text='Taux infection :').grid(row=row,column=0)
        self.entry_rate = Entry(self.fzom,width=5)
        self.entry_rate.grid(row=row,column=1)
        Button(self.fzom,text='valider',command=self.set_irate).grid(row=row,column=2)
        row+=1
        self.rate_label = Label(self.fzom,text='Actuellement : '+str(self.irate))
        self.rate_label.grid(row=row,column=0,columnspan=3)
        row+=1
        #zone 3.3
        Label(self.fzom,text='-------------------------------').grid(row=row,column=0,columnspan=3)
        row+=1
        Label(self.fzom,text='Durée de vie :').grid(row=row,column=0)
        self.entry_vie_zom = Entry(self.fzom,width=5)
        self.entry_vie_zom.grid(row=row,column=1)
        Button(self.fzom,text='Valider',command=self.set_zom_vie).grid(row=row,column=2)
        row+=1
        self.dureeVie_label = Label(self.fzom,text='Actuellement : '+str(self.dureeVie))
        self.dureeVie_label.grid(row=row,column=0,columnspan=3)
        row+=1
        #zone 3.4
        Label(self.fzom,text='-------------------------------').grid(row=row,column=0,columnspan=3)
        row+=1
        Label(self.fzom,text='Vitesse : ').grid(row=row,column=0)
        self.entry_v_zom = Entry(self.fzom,width=5)
        self.entry_v_zom.grid(row=row,column=1)
        Button(self.fzom,text='Valider',command=self.set_vzom).grid(row=row,column=2)
        row+=1
        self.vzom_label = Label(self.fzom,text='Actuellement : '+str(self.v_zom))
        self.vzom_label.grid(row=row,column=0,columnspan=3)
        self.fzom.grid(row=0,column=2,rowspan=3,sticky=N)
        
        #contrôle zone 4 : temps
        self.ftemps = Frame(self)
        Label(self.ftemps,text='--------------------Temps---------------------').grid(row=0,column=0,columnspan=3)
        Button(self.ftemps,text='demmarer',command=self.activer).grid(row=2,column=0)
        Button(self.ftemps,text='stop',command=self.desactiver).grid(row=2,column=1)
        Button(self.ftemps,text='nettoyer',command=self.reset).grid(row=2,column=2)
        self.run_label = Label(self.ftemps,text='Pause')
        self.run_label.grid(row=3,column=0,columnspan=3)
        self.ftemps.grid(row=1,column=1,sticky=N)
        
        # Setups prédéfinis
        Button(self,text='Setup 1',command=self.setup_1,).grid(row=2,column=1)
        
    # Méthodes modification de paramètres
    def modif_size(self):
        self.bati_sizex,self.bati_sizey = max(2*epaisseur,int(self.entry_sizex.get())),max(2*epaisseur,int(self.entry_sizey.get()))
        self.label_size.config(text='Actuellement : \n largeur '+str(self.bati_sizex)+' \n hauteur '+str(self.bati_sizey))

    def set_irate(self):
        self.irate=float(self.entry_rate.get())
        self.rate_label.config(text='Actuellement : '+str(self.irate))
        
    def set_zom_vie(self):
        m=self.entry_vie_zom.get()
        self.dureeVie=int(m)
        self.dureeVie_label.config(text='Actuellement : '+str(self.dureeVie))
        
    def set_hspawn(self):
        self.n_hspawn=self.entry_hspawn.get()    # Enregistre la zone de spawn des humains
        self.hspawn_label.config(text='Actuellement : '+self.n_hspawn)
        
    def set_zspawn(self):
        self.n_zspawn=self.entry_zspawn.get()     # Enregistre la zone de spawn des zombies
        self.zspawn_label.config(text='Actuellement : '+self.n_zspawn)
        
    def set_vhum(self):
        self.v_hum=int(self.entry_v_hum.get())
        self.vhum_label.config(text='Actuellement : '+self.entry_v_hum.get())
        
    def set_vzom(self):
        self.v_zom=int(self.entry_v_zom.get())
        self.vzom_label.config(text='Actuellement : '+str(self.v_zom))
        
    # Méthodes d'ajout d'éléments
    def ajout_batiment(self,event):
        x,y=self.bati_sizex,self.bati_sizey
        c1,c2=[event.x-x/2,event.y-y/2],[event.x+x/2,event.y+y/2]
        ok=True
        if not (0<=c1[0] and c2[0]<=fen_size[0] and 0<=c1[1] and c2[1]<=fen_size[1]):
            ok=False
        else:
            for bati in self.archi:
                if bati.test(c1,c2):
                    ok=False
        if ok:
            self.archi.append(batiment(self,c1,c2,len(self.archi)+1))
            
    def hspawn(self):
        if (not self.archi == []) and int(self.n_hspawn)<=len(self.archi):
            n=int(self.entry_hum.get())
            for i in range (n):
                if self.n_hspawn =='*':
                    bati=self.archi[randint(0,len(self.archi)-1)]
                else:
                    bati=self.archi[int(self.n_hspawn)-1]
                x,y=bati.c1[0]+5+random()*(bati.c2[0]-bati.c1[0]-10),bati.c1[1]+5+random()*(bati.c2[1]-bati.c1[1]-10)
                self.pop.append(humain(self,[x,y],self.v_hum,bati,self.id))
                self.id+=1

    def zspawn(self):
        if (not self.archi == []) and int(self.n_zspawn)<=len(self.archi):
            n=int(self.entry_zom.get())
            for i in range (n):
                if self.n_zspawn == '*':
                    bati=self.archi[randint(0,len(self.archi)-1)]
                else:
                    bati=self.archi[int(self.n_zspawn)-1]
                x,y=bati.c1[0]+5+random()*(bati.c2[0]-bati.c1[0]-10),bati.c1[1]+5+random()*(bati.c2[1]-bati.c1[1]-10)
                self.infec.append(zombie(self,[x,y],self.v_zom,bati,self.id,self.dureeVie))
                self.id+=1
          
    # Méthodes de retrait d'éléments
    def reset(self):
        for bati in self.archi:
            self.can.delete(bati.rect)
            self.can.delete(bati.label)
        self.archi=[]
        while self.pop != []:
            h=self.pop[0]
            self.retire(h.id,'h')
            self.can.delete(h.point)
        while self.infec != []:
            z=self.infec[0]
            self.retire(z.id,'z')
            self.can.delete(z.point)
                
    def retire(self,ide,m):
        if m=='h':
            for h in self.pop:
                if h.id==ide:
                    self.pop.remove(h)
        else:
            for z in self.infec:
                if z.id==ide:
                    self.infec.remove(z)
        
    #Mouvement
    def move(self):
        for z in self.infec:
            z.move(self.t)
        for h in self.pop:
            h.move(self.t)
            
    def run(self):
        if self.actif:
            self.move()
            self.after(int(self.t*200),self.run)
            
    def activer(self):
        self.actif=True
        self.run_label.config(text='En marche')
        self.run()
        
    def desactiver(self):
        self.actif=False
        self.run_label.config(text='Pause')

F=fenetre()
F.mainloop()
