class Cell():
    def __init__(self,x,y, content=0, sound=0):
        self.x=x
        self.y=y
        self.content=content
        self.sound=sound
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

