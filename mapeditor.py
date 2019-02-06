from tkinter import *
from casesMur import line

def isin(a,b,c):	# Return boolean : point a is in the rectangle with corner points b and c
	return (b[0]<=a[0]<=c[0] or c[0]<=a[0]<=b[0]) and (b[1]<=a[1]<=c[1] or c[1]<=a[1]<=b[1])
	

class Map_editor(Tk):
	def __init__(self):
		Tk.__init__(self)

		# Data
		self.x_size=15    # In cells
		self.y_size=15    # In cells
		self.ppc=30         # pixel per cell
		self.onclic='w'    # what to do when the user clic on a cell
		self.nclic = 1     # first or second clic for a new wall of line
		self.firstcase = (0,0)     # first clic for a wall of line
		self.grid=[[[0,0,0] for _ in range (self.y_size)] for _ in range (self.x_size)]
		self.nbati=1
		self.batiments=[]
		# Each cell is [x,y,z] where y is noise level and z is wall/not wall

		#Canvas
		self.canvas = Canvas(self,width=self.x_size*self.ppc,height=self.y_size*self.ppc)
		self.canvas.grid(row=0,column=0,rowspan=10)

		#Save/Open
		self.frame1 = Frame(self)
		self.filename_label = Label(self.frame1,text='Nom de la carte (no file extension)')
		self.filename_entry = Entry(self.frame1)
		self.frame2 = Frame(self)
		self.finish_button = Button(self.frame2,text='Sauvegarder',command=self.finish)
		self.open_button = Button(self.frame2,text='Ouvrir',command=self.load)
		self.clear_button = Button(self.frame2,text='Nettoyer',command=self.clear)
		self.frame3 = Frame(self)
		self.onclic_label = Label(self.frame3,text='Cliquer pour ajouter un mur')
		self.onclicwall_button = Button(self.frame3,text='Mur au clic',command=lambda: self.finish('w'))
		self.onclicline_button = Button(self.frame3,text='Ligne au clic',command=lambda: self.setclic('wl'))
		self.onclicbuild_button = Button(self.frame3,text='Batiment au clic',command=lambda: self.setclic('b'))

		#Layout
		self.frame1.grid(row=0,column=1)
		self.filename_label.grid(row=0,column=0)
		self.filename_entry.grid(row=1,column=0)

		self.frame2.grid(row=1,column=1)
		self.finish_button.grid(row=0,column=0)
		self.open_button.grid(row=1,column=0)
		self.clear_button.grid(row=2,column=0)

		self.frame3.grid(row=2,column=1)
		Label(self.frame3,text='------').grid(row=0,column=0)
		self.onclic_label.grid(row=1,column=0)
		self.onclicwall_button.grid(row=2,column=0)
		self.onclicline_button.grid(row=3,column=0)
		self.onclicbuild_button.grid(row=4,column=0)

		# Binding
		self.canvas.bind('<Button-1>',self.clic)
		self.canvas.bind('<Button-3>',self.rclic)
		self.bind('Escape',self.leave)

	def clic(self,event):
		nx,ny=event.x//self.ppc,event.y//self.ppc
		if self.onclic == 'w':
			self.add_wall(nx,ny)
		elif self.onclic == 'wl':
			if self.nclic == 1:
				self.firstcase = (nx,ny)
				self.nclic+=1
			else:
				self.add_line(self.firstcase[0],self.firstcase[1],nx,ny)
				self.nclic-=1
		elif self.onclic == 'b':
			
			if self.nclic == 1:
				self.firstcase = (nx,ny)
				self.nclic+=1
			elif self.nclic == 2:
				self.nclic +=1
				self.add_build(self.firstcase[0],self.firstcase[1],nx,ny)
			else:
				self.adddoor(nx,ny)
			
	def rclic(self,event):
		self.nclic = 1
		self.nbati += 1

	def add_line(self,nx1,ny1,nx2,ny2):
		L=line(nx1,ny1,nx2,ny2)
		for case in L:
			self.add_wall(case[0],case[1])

	def add_wall(self,nx,ny):
		self.grid[nx][ny][2]=1
		self.color(nx,ny,'black')
		
	def add_wallinbati(self,nx,ny):
		self.grid[nx][ny][2]=1
		self.grid[nx][ny][0]=self.nbati
		self.color(nx,ny,'black')
		
	def adddoor(self,nx,ny):
		if self.grid[nx][ny][0] == self.nbati:
			self.grid[nx][ny][2]=2
			self.color(nx,ny,'blue')
		self.batiments[self.nbati-1].append(nx)
		self.batiments[self.nbati-1].append(ny)

	def add_build(self,nx1,ny1,nx2,ny2):
		for nx in range (min(nx1,nx2),max(nx1,nx2)+1):
			self.add_wallinbati(nx,min(ny1,ny2))
			self.add_wallinbati(nx,max(ny1,ny2))
		for ny in range (min(ny1,ny2),max(ny1,ny2)+1):
			self.add_wallinbati(min(nx1,nx2),ny)
			self.add_wallinbati(max(nx1,nx2),ny)
		self.batiments.append([nx1,ny1,nx2,ny2])

	def color(self,nx,ny,color):
		self.canvas.create_rectangle(nx*self.ppc,ny*self.ppc,(nx+1)*self.ppc-1,(ny+1)*self.ppc-1,fill=color)

	def finish(self):
		filename='saves/'+self.filename_entry.get()
		if filename != '':
			g=self.grid
			with open(filename+'.txt',"w") as f:
				for i in range(len(g)):
					for j in range(len(g[0])-1):
						f.write(str(g[i][j][0])+'/'+str(g[i][j][1])+'/'+str(g[i][j][2])+' ')
					f.write(str(g[i][j][0])+'/'+str(g[i][j][1])+'/'+str(g[i][j][2])+'\n')
				for i in range (len(self.batiments)):
					for j in range (len(self.batiments[i])-1):
						f.write(str(self.batiments[i][j])+'/')
					f.write(str(self.batiments[i][-1]))
					if i!=len(self.batiments)-1:
						f.write(' ')

	def load(self):
		filename='saves/'+self.filename_entry.get()
		try:
			with open(filename+'.txt',"r") as f:
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
			self.batiments=[b.split('/') for b in batiments]
		except:
			pass

	def clear(self):
		self.grid=[[[0,0,0] for _ in range (self.y_size)] for _ in range (self.x_size)]
		self.nclic=1
		self.onclic = 'w'    # wl for wall line
		self.onclic_label.config(text='Cliquer pour ajouter un mur')
		self.canvas.delete("all")
		self.batiments=[]

	def setclic(self,txt):  # change from one wall per clic to a line of wall per two clics
		self.nclic=1
		if txt == 'w':
			self.onclic = 'w'    # wl for wall line
			self.onclic_label.config(text='Cliquer pour ajouter un mur')
		elif txt == 'wl':
			self.onclic = 'wl'
			self.onclic_label.config(text='Cliquer deux fois pour \n une ligne de murs')
		elif txt == 'b': 
			self.onclic = 'b'
			self.onclic_label.config(text='Cliquer deux fois pour \n un batiment, puis une \n fois pour la porte, \n puis clic droit')
	def leave(self,event):
		self.destroy()

E=Map_editor()
E.focus_force()
E.mainloop()
