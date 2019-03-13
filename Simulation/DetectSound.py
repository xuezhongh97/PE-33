def detectSound(self,G,x,y):
    u,v=0,0
    if x>0:
    	u-=G[x-1][y].sound
    	if y>0:
    		u-=G[x-1][y-1].sound/2**0.5
    	if y<yMax:
    		u-=G[x-1][y+1].sound/2**0.5

    if x<xMax-1:
    	u+=G[x+1][y].sound
    	if y>0:
    		u-=G[x+1][y-1].sound/2**0.5
    	if y<yMax:
    		u-=G[x+1][y+1].sound/2**0.5

    if y>0:
    	v-=G[x][y-1].sound
    if y<yMax:
    	v+=G[x][y+1].sound

    return(u,v)
    #pas pris en compte hearing et le son en (x,y) ici