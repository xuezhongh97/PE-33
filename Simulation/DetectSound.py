def DetectSound(G,x,y,R):
    L=[0,0]
    for i in range(x-R,x+R+1):
        for j in range(y-R,y+R+1):
            r=((i-x)**2+(j-y)**2)**(1/2)
            if r<=R and r!=0:
                L[0]+=G[i][j]*(i-x)/r
                L[1]+=G[i][j]*(j-y)/r
    return(L)
