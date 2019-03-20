from Parameters import *
from Cell import *
from CreateBeing import *

class Master:
    def __init__(self):
        self.Map=[]
        self.Humans=[]
        self.Zombies=[]

Master=Master()

""" Map creation """
Master.Map=[[Cell(i,j) for j in range(ySize)] for i in range(xSize)]
Buildings=[]

with open("Map/"+mapTxt, "r") as f:
    lines=f.read().split("\n")
for i in range(xSize):
    line=list(lines[i].split())
    for j in range(ySize):
        cell=list(line[j].split("/"))
        Master.Map[i][j].idBuilding=int(cell[0])
        Master.Map[i][j].sound=int(cell[1])
        Master.Map[i][j].content=int(cell[2])

for _ in range(nZombies):
    Master.Zombies.append(create_zombie(Master))

for _ in range(nHumans):
    Master.Humans.append(create_human(Master))

""" Simulation """
t=1
while t<=Tsimulation:
    print("======== Tour {} ========".format(t))
    for nh in range(len(Master.Humans)-1, -1, -1):
        h=Master.Humans[nh]
        h.action()
        h.info()
    print()
    for nz in range(len(Master.Zombies)-1,-1,-1):
        z=Master.Zombies[nz]
        z.action()
        z.info()
        print(z.lifespan)
    t+=dt
    print()