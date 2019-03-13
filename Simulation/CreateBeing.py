#Zombie paramaters
z_speed=1
z_vision=1
z_hearing=1
z_strength=1
z_agility=1
z_lifespan=1
z_incubation_time=10

#Human parameters
h_vision=1
h_hearing=1

weak, casual, strong=(1,1,1), (2,2,2), (3,3,3) #speed, strength, agility
pAbilities=[1/4, 1/2, 1/4] #proba for general stats

evil, neutral, hero=0,1,2
pMoralities=[1/4, 1/2, 1/4] #proba

flee,hide,fight=0,1,2
pBehaviors=[1/3, 1/3, 1/3]  #proba

zen,stable,stressed=0,1,2
pStress=[1/3, 1/3, 1/3] #proba

def create_zombie():
    x,y=randint(0, xSize-1), randint(0, ySize-1)
    while Carte[x][y].content!=0:
        x,y=randint(0, xSize-1), randint(0, ySize-1)

    return(Zombie((x,y),z_speed,z_vision,z_hearing,z_strength,z_agility,z_lifespan))

for _ in range(nZombies):
    Zombies.append(create_zombie())

def create_human():
    ability=random()
    if ability<=pAbilities[0]:
        ability=weak
    elif ability<=pAbilities[1]+pAbilities[0]:
        ability=casual
    else:
        ability=strong

    morality=random()
    if morality<=pMoralities[0]:
        morality=evil
    elif morality<=pMoralities[1]+pMoralities[0]:
        morality=neutral
    else:
        morality=hero

    behavior=random()
    if behavior<=pBehaviors[0]:
        behavior=flee
    elif behavior<=pBehaviors[1]+pBehaviors[0]:
        behavior=hide
    else:
        behavior=fight

    coldblood=random()
    if coldblood<=pStress[0]:
        coldblood=zen
    elif coldblood<=pStress[1]+pStress[0]:
        coldblood=stable
    else:
        coldblood=stressed

    x,y=randint(0, xSize-1), randint(0, ySize-1)
    while Carte[x][y].content!=0:
        x,y=randint(0, xSize-1), randint(0, ySize-1)

    return(Human((x,y),ability[0],h_vision,h_hearing, ability[1], ability[2], coldblood, morality, behavior))