from Parameters import *
from Cell import *
from CreateBeing import *

""" Map creation """
Buildings=[]
Map=[[Cell(i,j) for j in range(ySize)] for i in range(xSize)]

with open("Map/"+mapTxt, "r") as f:
    lines=f.read().split("\n")
for i in range(xSize):
    line=list(lines[i].split())
    for j in range(ySize):
        cell=list(line[j].split("/"))
        Map[i][j].idBuilding=int(cell[0])
        Map[i][j].sound=int(cell[1])
        Map[i][j].content=int(cell[2])

""" Beings creation """
Humans=[]
Zombies=[]

for _ in range(nZombies):
    Zombies.append(create_zombie(Map))

for _ in range(nHumans):
    Humans.append(create_human(Map))

""" Simulation """
t=0
while t<Tsimulation:
    for h in Humans:
        h.action()
    for z in Zombies:
        z.action()
    t+=dt
