from Definitions import *
class Level:
    def __init__(self,name,dimension,level,foreground,background,endPos,startPos=(1,1,1,1)):
        self.name=name
        self.dimension=dimension
        self.size=len(level)
        self.foreground=foreground
        self.background=background
        self.endPos=endPos
        self.startPos=startPos
        self.level=level
        endPos+=[1,1]
        self.level[endPos[0],endPos[1],endPos[2],endPos[3]]=0
    def __getitem__(self,*index):
        index=index[0]
        x,y=index[:2]
        try:
            item=self.level[x,y,1,1]
            item=self.level[x,y,index[2],1]
            item=self.level[x,y,index[2],index[3]]
        except TypeError:
            pass
        return item
class Player:
    inMove=0
    dx=0
    dy=0
    dz=0
    dw=0
    moveTime=8
    def __init__(self,x,y,z,w):
        self.x=x
        self.y=y
        self.z=z
        self.w=w
    def move(self,level,dx=0,dy=0,dz=0,dw=0):
        self.inMove=self.moveTime
        try:
            wall=level[self.x+dx,self.y+dy,self.z+dz,self.w+dw]
        except IndexError:
            wall=0
        if wall:
            self.inMove=0
        self.dx=dx
        self.dy=dy
        self.dz=dz
        self.dw=dw
    def getIntPos(self):
        return(int(self.x),int(self.y),int(self.z),int(self.w))
    def getPos(self):
        return(self.x,self.y,self.z,self.w)
    def update(self,state):
        keys=pygame.key.get_pressed()
        if not self.inMove:
            move=None
            if keys[pygame.K_UP]or keys[pygame.K_w]:
                move=(0,-1)
            if keys[pygame.K_DOWN]or keys[pygame.K_s]:
                move=(0,1)
            if keys[pygame.K_LEFT]or keys[pygame.K_a]:
                move=(-1,0)
            if keys[pygame.K_RIGHT]or keys[pygame.K_d]:
                move=(1,0)
            if move:
                self.move(state.level,*orientPos(state.orient,(0,0,0,0),move))
        if self.inMove:
            factor=2*self.inMove/(self.moveTime**2+self.moveTime)
            self.x+=self.dx*factor
            self.y+=self.dy*factor
            self.z+=self.dz*factor
            self.w+=self.dw*factor
            self.inMove-=1
            if self.inMove==0:
                self.x=round(self.x)
                self.y=round(self.y)
                self.z=round(self.z)
                self.w=round(self.w)
