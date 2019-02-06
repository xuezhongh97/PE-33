class Cell():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.content=0
        self.sound=0
        self.humains=[]
        self.zombies=[]

    def __str__(self):
        if self.content==0:
            print(".")
        else:
            print("#")

    def affiche(self):
        print("x:",self.x," y:",self.y)
        print("content:",self.content, "sound:",self.sound)
        print("humains:")
        for h in self.humains:
            print(h)
        print("zombies:")
        for z in self.zombies:
            print(z)

