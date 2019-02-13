from tkinter import *
import numpy

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
		self.humains=[]
		self.zombies=[]
		# Each cell is [x,y,z] where y is noise level and z is wall/not wall

		#Canvas
		self.canvas = Canvas(self,width=self.x_size*self.ppc,height=self.y_size*self.ppc,bg='white')
		self.canvas.grid(row=0,column=0,columnspan=4)
		self.testbut = Button(self,text="Test",command=lambda: self.plot_humain([(13,13),(24,4)]))
		self.testbut.grid(row=1,column=1)
		self.testbut2 = Button(self,text="Test2",command=lambda: self.plot_zombie([(20,5),(20,31)]))
		self.testbut2.grid(row=1,column=2)
		
		# Load map
		self.load()
		
		# Binding
		self.canvas.bind('<Button-1>',self.clic)
		
	def load(self):
		with open('saves/Map.txt',"r") as f:
			text=f.read()
		lines=text.split('\n')
		batis=lines[-1]
		lines=lines[0:len(lines)-1]
		self.grid=[lines[i].split(' ') for i in range(len(lines))]
		self.x_size=len(self.grid[0])
		self.y_size=len(self.grid)
		self.ppc=int(min(self.winfo_screenwidth()/self.y_size,self.winfo_screenheight()/self.x_size))
		self.canvas.delete("all")
		self.canvas.config(width=self.ppc*self.y_size,height=self.ppc*self.x_size)
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
				elif self.grid[i][j][2]==3:
					self.color(i,j,'yellow')
				elif self.grid[i][j][2]==4:
					self.color(i,j,'green')
		batims=batis.split(' ')
		self.batiments=[b.split('/') for b in batims]
		
	def color(self,nx,ny,color):
		self.canvas.create_rectangle(nx*self.ppc,ny*self.ppc,(nx+1)*self.ppc-1,(ny+1)*self.ppc-1,fill=color,outline=color)

	def genSound(self,x0,y0,volume):
		xMax,yMax=self.y_size,self.x_size
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
					if x>=0 and x<xMax and y>=0 and y<yMax and (self.grid[x][y][2]==0 or self.grid[x][y][2]==2)  and not(visited[x-x0+volume][y-y0+volume]) and value>0:
						self.grid[x][y][1]+=round(value)
						visited[x-x0+volume][y-y0+volume]=True
						self.color(x,y,self.reform(self.grid[x][y][1]))
						new.append((x,y,value))
			suivants=new[:]
				
	def reform(self,n):
		#num=int(500/numpy.pi*numpy.arctan(0.5*n))
		num=int(250*(1-numpy.exp(-n/5)))
		txt=hex(255-num)[2:]
		if len(txt)==1:
			txt='0'+txt
		return('#ff'+txt+txt)
		
	def plot_humain(self,L):
		d=int(self.ppc/3.5)
		for oval in self.humains:
			self.canvas.delete(oval)
		self.humains=[]
		for (x,y) in L:
			px,py=int(self.ppc*x),int(self.ppc*y)
			self.humains.append(self.canvas.create_oval(px-d,py-d,px+d,py+d,fill='#ba4a00'))
			
	def plot_zombie(self,L):
		d=int(self.ppc/3.5)
		for oval in self.zombies:
			self.canvas.delete(oval)
		self.zombies=[]
		for (x,y) in L:
			px,py=int(self.ppc*x),int(self.ppc*y)
			self.zombies.append(self.canvas.create_oval(px-d,py-d,px+d,py+d,fill='#4a235a'))

	def clic(self,event):
		self.genSound(int(event.x/self.ppc),int(event.y/self.ppc),8)
			
E=Visualisator()
E.focus_force()
E.mainloop()