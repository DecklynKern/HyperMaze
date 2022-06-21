from Generation import *
class Button:
    hovered=False
    def __init__(self,x,y,text,function,colour1=(128,128,128),colour2=(220,220,255)):
        self.x=x
        self.y=y
        self.text=text
        self.img1=font1.render(text,1,colour1)
        self.img2=font1.render(text,1,colour2)
        self.width,self.height=self.img1.get_size()
        self.x-=self.width//2
        self.y-=self.height//2
        self.function=function
        self.colour1=colour1
        self.colour2=colour2
    def render(self,screen):
        colour=self.colour1
        img=self.img1
        if self.hovered:
            colour=self.colour2
            img=self.img2
        pygame.draw.rect(screen,colour,(self.x-7,self.y-7,self.width+14,self.height+14),6)
        screen.blit(img,(self.x,self.y))
def resumeGame():
    state.mainMenu=0
    state.pauseMenu=False
    state.buttons=[]
    switchMusic("bensound-psychedelic.ogg")
    state.fadeout=255
    state.image.blit(screen,(0,0))
def playGame():
    resumeGame()
    state.procedural=False
    state.orient=0
    state.player=Player(1,1,1,1)
    loadLevel(str(state.levelNum))
def selectLevel(num):
    def helper():
        state.levelNum=num
        playGame()
    return helper
def levelSelect():
    state.buttons=[
        Button(100,300,"Back",mainMenu),
    ]+[Button(125+75*n,300," %s "%n,selectLevel(n))for n in range(1,state.maxLevel+1)]
def generator():
    resumeGame()
    state.orient=0
    state.player=Player(1,1,1,1)
    state.procedural=True
    state.proceduralLevel=1
    switchMusic("460524__lokna85__melody-z-2.wav")
    generateLevel()
def optionsMenu():
    state.buttons=[
        Button(420,400,"lol",lambda:0),
        Button(420,500,"Back",closeOptionsMenu),
    ]
def closeOptionsMenu():
    if state.mainMenu:
        mainMenu()
    else:
        pauseMenu()
def stop():
    state.done=True
def pauseMenu():
    state.pauseMenu=True
    state.buttons=[
        Button(420,300,"Main Menu",mainMenu),
        Button(420,400,"Options",optionsMenu),
        Button(420,500,"Back",resumeGame)
    ]
def mainMenu():
    state.mainMenu=1
    state.pauseMenu=False
    state.buttons=[
        Button(420,350,"Play Game",playGame),
        Button(420,450,"Level Select",levelSelect),
        Button(420,550,"Generator Mode",generator),
        Button(420,650,"Options",optionsMenu),
        Button(420,750,"Quit",stop),
    ]
    switchMusic("bensound-endlessmotion.ogg")
