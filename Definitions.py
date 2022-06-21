import pygame,pygame.gfxdraw,math,os,pprint,numpy,random,opensimplex,threading
pygame.init()
clock=pygame.time.Clock()
screenSize=840
font1=pygame.font.Font("fonts\\iomanoid front.ttf",48)
font2=pygame.font.Font("fonts\\iomanoid front.ttf",18)
screen=pygame.display.set_mode((screenSize,screenSize+100))
pygame.display.set_caption("HyperMaze")
title=pygame.image.load("images\\title.png").convert()
title.set_colorkey((0,0,0))
background1=pygame.image.load("images\\background1.png").convert()
background2=pygame.image.load("images\\background2.png").convert()
background3=pygame.image.load("images\\background3.png").convert()
background4=pygame.image.load("images\\background4.png").convert()
flipSound=pygame.mixer.Sound("sounds\\flip.wav")
blipSound=pygame.mixer.Sound("sounds\\blip.wav")
noise=opensimplex.OpenSimplex(0)
null=lambda:0
t=0
class State:
    procedural=False
    pauseMenu=False
    maxLevel=1
    levelNum=1
    proceduralLevel=1
    mainMenu=0
    buttons=[]
    orient=0 #xy, xz, yz, xw, yw, zw
    done=False
    music="temp"
    image=pygame.Surface((screenSize,screenSize))
    fadeout=0
state=State()
def thread(func):
    def helper(*args,**kwargs):
        func(*args,**kwargs)
    return helper
def drawCircle(surf,colour,x,y,r):
    x=int(x)
    y=int(y)
    r=int(r)
    pygame.gfxdraw.aacircle(surf,x,y,r,colour)
    pygame.gfxdraw.filled_circle(surf,x,y,r,colour)
def orientToAxis(orient):
    if orient==0:
        return(1,2,0,0)
    elif orient==1:
        return(1,0,2,0)
    elif orient==2:
        return(0,1,2,0)
    elif orient==3:
        return(1,0,0,2)
    elif orient==4:
        return(0,1,0,2)
    elif orient==5:
        return(0,0,1,2)
def orientPos(orient,playerPos,pos):
    axis=orientToAxis(orient)
    return tuple(pos[axis[n]-1]if axis[n]!=0 else playerPos[n] for n in range(4))
def flattenPos(orient,pos):
    finalPos=[0,0]
    axis=orientToAxis(orient)
    for n in range(4):
        if axis[n]:
            finalPos[axis[n]-1]=pos[n]
    return tuple(finalPos)
@thread
def switchMusic(name):
    if state.music!=name:
        state.music=name
        pygame.mixer.fadeout(750)
        pygame.mixer.music.load("sounds\\%s"%name)
        pygame.mixer.music.play(-1)
