#carte[x][y][idBatiment, sound, 1 si mur]

def genSound(x0,y0,volume):
    if x0<0 or x0>=xMax or y0<0 or y0>=yMax:
        print("error")
        return()

    carte[x0][y0].sound=volume
    if volume==1:
        return()
    moves=[(0,1), (0,-1), (1,0), (-1,0), (-1,-1), (-1,1), (1,-1), (1,1)]
    suivants=[(x0,y0,volume)]

    while suivants:
        new=[]
        for a,b,M in suivants:
            for dx,dy in moves:
                x,y=a+dx,b+dy
                value=M-(dx**2+dy**2)**(1/2)
                if x>=0 and x<xMax and y>=0 and y<yMax and carte[x][y].mur==0 and carte[x][y].sound<value and value>0:
                    carte[x][y].sound=round(value)
                    new.append((x,y,value))
        suivants=new[:]


if __name__=="__main__":
    class Case():
        def __init__(self, mur):
            self.sound=0
            self.mur=mur

        def __str__(self):
            if self.mur!=0:
                return("#")
            return(str(self.sound))

    xMax,yMax=10,10
    carte=[[Case(0) for _ in range(yMax)] for _ in range(xMax)]
    for k in range(4):
        carte[k][2].mur=1

    genSound(0,0,9)

    for x in range(xMax):
        for y in range(yMax):
            print(carte[x][y], end=" ")
        print("\n")