def bruit(x,y,M):
	# savoir si les parametres sont correctes
	if x<0 or x>cartemax or y<0 or y>cartemax:
		print("error")
		return 0
	carte[x][y][1]+=M

	for j in range(1,M):
		for k in range(1,M):
			if distance(j,k)<=M:
				if isout(x-j,y-k)==1:
					carte[x-j][y-k][1]+=M-int(distance(j,k))
				if isout(x+j,y-k)==1:
					carte[x+j][y-k][1]+=M-int(distance(j,k))
				if isout(x+j,y+k)==1:
					carte[x+j][y+k][1]+=M-int(distance(j,k))
				if isout(x-j,y+k)==1:
					carte[x-j][y+k][1]+=M-int(distance(j,k))
	for j in range(1,M):
		carte[x+j][y][1]+=M-j
		carte[x-j][y][1]+=M-j 
	for j in range(1,M):
		carte[x][y+j][1]+=M-j
		carte[x][y-j][1]+=M-j
	trouvermur(x,y,M)                           
def isout(x,y):
	if x<0 or x>cartemax or y<0 or y>cartemax:
		return 0
	return 1

def distance(x,y):
	return math.sqrt(pow(x,2)+pow(y,2))

def addmur(x1,y1,x2,y2):
	for i in range(x1,x2+1):
		for j in range(y1,y2+1):
			carte[i][j][2]=1
def angle(x,y,m,n):
	return math.atan((y-n)/(x-m))

def trouvermur(x,y,M):
	maxangle=-10
	minangle=10
	angle1=0
	angle2=0
	distancemur=0
	for i in range(x+1,x+M+1):
		for j in range(y-M,y+M+1):
			if carte[i][j][2]==1 and carte[i+1][j][2]==1:
				angle1=angle(i,j,x,y)
				angle2=angle(i+1,j,x,y)
				maxangle=max(angle1,angle2)
				minangle=min(angle1,angle2)
				distancemur=distance(i+1-x,j-y)
				for k in range(x+1,x+M+1):
					for l in range(y-M,y+M+1):
						if distance(k-x,l-y)>=distancemur and angle(k,l,x,y)<=maxangle and angle(k,l,x,y)>=minangle:
							carte[k][l][1]=0
			elif carte[i][j][2]==1 and carte[i][j+1][2]==1:
				angle1=angle(i,j+1,x,y)
				angle2=angle(i,j,x,y)
				maxangle=max(angle1,angle2)
				minangle=min(angle1,angle2)
				distancemur=distance(i-x,j+1-y)
				for k in range(x+1,x+M+1):
					for l in range(y-M,y+M+1):
						if distance(k-x,l-y)>=distancemur and angle(k,l,x,y)<=maxangle and angle(k,l,x,y)>=minangle:
							carte[k][l][1]=0	
	for i in range(x-M,x):
		for j in range(y-M,y+M+1):
			if carte[i][j][2]==1 and carte[i-1][j][2]==1:
				angle1=angle(i,j,x,y)
				angle2=angle(i-1,j,x,y)
				maxangle=max(angle1,angle2)
				minangle=min(angle1,angle2)
				distancemur=distance(i-1-x,j-y)
				for k in range(x-M,x):
					for l in range(y-M,y+M+1):
						if distance(k-x,l-y)>=distancemur and angle(k,l,x,y)<=maxangle and angle(k,l,x,y)>=minangle:
							carte[k][l][1]=0
			elif carte[i][j][2]==1 and carte[i][j-1][2]==1:
				angle1=angle(i,j-1,x,y)
				angle2=angle(i,j,x,y)
				maxangle=max(angle1,angle2)
				minangle=min(angle1,angle2)
				distancemur=distance(i-x,j-1-y)
				for k in range(x-M,x):
					for l in range(y-M,y+M+1):
						if distance(k-x,l-y)>=distancemur and angle(k,l,x,y)<=maxangle and angle(k,l,x,y)>=minangle:
							carte[k][l][1]=0
	i=x
	for j in range(y+1,y+M+1):
		if carte[i][j][2]==1 and carte[i-1][j][2]==1:
			for l in range(j,y+M+1):
				carte[i][l][1]=0
			angle1=-0.5*math.pi
			angle2=angle(i-1,j,x,y)
			maxangle=max(angle1,angle2)
			minangle=min(angle1,angle2)
			distancemur=distance(i-1-x,j-y)
			for k in range(x-M,x+M+1):
				if k!=x:
					for l in range(y,y+M+1):
						if distance(k-x,l-y)>=distancemur and angle(k,l,x,y)<=maxangle and angle(k,l,x,y)>=minangle:
							carte[k][l][1]=0
	for j in range(y+1,y+M+1):
		if carte[i][j][2]==1 and carte[i+1][j][2]==1:
			for l in range(j,y+M+1):
				carte[i][l][1]=0
			angle1=0.5*math.pi
			angle2=angle(i+1,j,x,y)
			maxangle=max(angle1,angle2)
			minangle=min(angle1,angle2)
			distancemur=distance(i+1-x,j-y)
			for k in range(x-M,x+M+1):
				if k!=x:
					for l in range(y,y+M+1):
						if distance(k-x,l-y)>=distancemur and angle(k,l,x,y)<=maxangle and angle(k,l,x,y)>=minangle:
							carte[k][l][1]=0
	for j in range(y-M,y):
		if carte[i][j][2]==1 and carte[i-1][j][2]==1:
			for l in range(y-M,j+1):
				carte[i][l][1]=0
			angle1=0.5*math.pi
			angle2=angle(i-1,j,x,y)
			maxangle=max(angle1,angle2)
			minangle=min(angle1,angle2)
			distancemur=distance(i-1-x,j-y)
			for k in range(x-M,x+M+1):
				if k!=x:
					for l in range(y-M,y):
						if distance(k-x,l-y)>=distancemur and angle(k,l,x,y)<=maxangle and angle(k,l,x,y)>=minangle:
							carte[k][l][1]=0
	for j in range(y-M,y):
		if carte[i][j][2]==1 and carte[i+1][j][2]==1:
			for l in range(y-M,j+1):
				carte[i][l][1]=0
			angle1=-0.5*math.pi
			angle2=angle(i+1,j,x,y)
			maxangle=max(angle1,angle2)
			minangle=min(angle1,angle2)
			distancemur=distance(i+1-x,j-y)
			for k in range(x-M,x+M+1):
				if k!=x:
					for l in range(y-M,y):
						if distance(k-x,l-y)>=distancemur and angle(k,l,x,y)<=maxangle and angle(k,l,x,y)>=minangle:
							carte[k][l][1]=0

import math
cartemax=20
carte=[[[0 for i in range(3)] for i in range(30)]for i in range(30)]
#chushihua
for i in range(0,cartemax):
	for j in range(0,cartemax):
		carte[i][j][1]=0
		carte[i][j][2]=0


addmur(7,3,12,4)
addmur(3,4,4,9)
addmur(13,5,15,12)
bruit(9,9,9)
bruit(13,13,7)

for i in range(0,cartemax+1):
	for j in range(0,cartemax):
		if carte[i][j][1]!=0:
			print(carte[i][j][1],end="  ")
		else:
			print('.',end="  ")
	print ('\n')
print ('\n')
for i in range(0,cartemax+1):
	for j in range(0,cartemax):
		if carte[i][j][2]!=0:
			print(carte[i][j][2],end="  ")
		else:
			print('.',end="  ")
	print ('\n')

