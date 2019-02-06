from tkinter import *

class Visualisator(Tk):
	def __init__(self):
		Tk.__init__(self)

		# Data
		self.x_size=15    # In cells
		self.y_size=15    # In cells
		self.ppc=30         # pixel per cell
		self.onclic='w'    # what to do when the user clic on a cell
		self.nclic = 1     # first or second clic for a new wall of line
		self.firstcase = (0,0)     # first clic for a wall of line
		self.grid=[]
		self.nbati=1
		self.batiments=[]
		# Each cell is [x,y,z] where y is noise level and z is wall/not wall

		#Canvas
		self.canvas = Canvas(self,width=self.x_size*self.ppc,height=self.y_size*self.ppc)
		self.canvas.grid(row=0,column=0,rowspan=10)
		
		# Load map
		self.load()
		
		# Binding
		self.canvas.bind('<Button-1>',self.clic)
		
	def load(self):
		with open('map.txt',"r") as f:
			text=f.read()
		lines=text.split('\n')
		batis=lines[-1]
		lines=lines[0:len(lines)-1]
		self.grid=[lines[i].split(' ') for i in range(len(lines))]
		self.canvas.delete("all")
		self.canvas.config(width=self.ppc*len(self.grid),height=self.ppc*len(self.grid[0]))
		self.nbati=1
		for i in range (len(self.grid)):
			for j in range (len(self.grid[0])):
				self.grid[i][j]=self.grid[i][j].split('/')
				for k in range (len(self.grid[i][j])):
					self.grid[i][j][k]=int(self.grid[i][j][k])
				if self.grid[i][j][2]==1:
					self.color(i,j,'black')
				elif self.grid[i][j][2]==2:
					self.color(i,j,'blue')
		batims=batis.split(' ')
		self.batiments=[b.split('/') for b in batims]
		
	def color(self,nx,ny,color):
		self.canvas.create_rectangle(nx*self.ppc,ny*self.ppc,(nx+1)*self.ppc-1,(ny+1)*self.ppc-1,fill=color)

	def genSound(self,x0,y0,volume):
		xMax,yMax=self.x_size,self.y_size
		if x0<0 or x0>xMax or y0<0 or y0>yMax:
			print("error")
			return
		self.grid[x0][y0][1]+=volume
		self.color(x0,y0,self.reform(round(self.grid[x0][y0][1])))
		if volume==1:
			return
		moves=[(0,1), (0,-1), (1,0), (-1,0), (-1,-1), (-1,1), (1,-1), (1,1)]
		suivants=[(x0,y0,volume)]
		
		visited=[[False for _ in range(2*volume+1)] for _ in range(2*volume+1)]
		visited[volume][volume]=True

		while suivants:
			new=[]
			for a,b,M in suivants:
				for dx,dy in moves:
					x,y=a+dx,b+dy
					value=M-(dx**2+dy**2)**(1/2)
					if x>=0 and x<=xMax and y>=0 and y<=yMax and self.grid[x][y][2]!=1 and not(visited[x-x0+volume][y-y0+volume]) and value>0:
						self.grid[x][y][1]+=round(value)
						visited[x-x0+volume][y-y0+volume]=True
						self.color(x,y,self.reform(round(self.grid[x][y][1])))
						new.append((x,y,value))
			suivants=new[:]
				
	def reform(self,n):
		txt=hex(255-20*n)[2:]
		if len(txt)==1:
			txt='0'+txt
		print(txt)
		return('#ff'+txt+txt)
		

	def clic(self,event):
		self.genSound(int(event.x/self.ppc),int(event.y/self.ppc),3)
			
E=Visualisator()
E.focus_force()
E.mainloop()