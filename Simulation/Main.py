from Cell import *
from Being import *
from DetectSound import *
from generateurSon import *
from random import random, randint

""" Parameters """
Tsimulation=10
dt=1
xSize=100
ySize=100
attenuation_porte=3

#Zombie paramaters
nZombies=1
z_speed=1
z_vision=1
z_hearing=1
z_strength=1
z_agility=1
z_lifespan=1
z_incubation_time=10

#Human parameters
nHumans=1
h_vision=1
h_hearing=1

weak, casual, strong=(1,1,1), (2,2,2), (3,3,3) #speed, strength, agility
Abilities=[1/4, 1/2, 1/4] #proba for general stats

evil, neutral, hero=0,1,2
Moralities=[1/4, 1/2, 1/4] #proba

flee,hide,fight=0,1,2
Behaviors=[1/3, 1/3, 1/3]  #proba

zen,stable,stressed=0,1,2
Stress=[1/3, 1/3, 1/3] #proba

""" Creation """
Carte=[[Cell(i,j) for j in range(ySize)] for i in range(xSize)]
Humans=[]
Zombies=[]
Buildings=[]

def create_zombie():
    x,y=randint(0, xSize-1), randint(0, ySize-1)
    while Carte[x][y].content!=0:
        x,y=randint(0, xSize-1), randint(0, ySize-1)

    return(Zombie((x,y),z_speed,z_vision,z_hearing,z_strength,z_agility,z_lifespan))

for _ in range(nZombies):
    Zombies.append(create_zombie())

def create_human():
    ability=random()
    if ability<=Abilities[0]:
        ability=weak
    elif ability<=Abilities[1]+Abilities[0]:
        ability=casual
    else:
        ability=strong

    morality=random()
    if morality<=Moralities[0]:
        morality=evil
    elif morality<=Moralities[1]+Moralities[0]:
        morality=neutral
    else:
        morality=hero

    behavior=random()
    if behavior<=Behaviors[0]:
        behavior=flee
    elif behavior<=Behaviors[1]+Behaviors[0]:
        behavior=hide
    else:
        behavior=fight

    coldblood=random()
    if coldblood<=Stress[0]:
        coldblood=zen
    elif coldblood<=Stress[1]+Stress[0]:
        coldblood=stable
    else:
        coldblood=stressed

    x,y=randint(0, xSize-1), randint(0, ySize-1)
    while Carte[x][y].content!=0:
        x,y=randint(0, xSize-1), randint(0, ySize-1)

    return(Human((x,y),ability[0],h_vision,h_hearing, ability[1], ability[2], coldblood, morality, behavior))

for _ in range(nHumans):
    Humans.append(create_human())

""" Simulation """
t=0
while t<Tsimulation:
    t+=dt
    for h in Humans:
        h.action()
    for z in Zombies:
        z.action()
