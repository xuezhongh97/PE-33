def detectSound(G,x,y,R):
    u,v=0,0
    for i in range(x-R,x+R+1):
        for j in range(y-R,y+R+1):
            r=((i-x)**2+(j-y)**2)**(1/2)
            if r<=R and r!=0:
                volume=G[i][j].sound
                u+=volume*(i-x)/r
                v+=volume*(j-y)/r
    return(u,v)