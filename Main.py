from GUI import *
mainMenu()
while not state.done:
    t+=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            state.done=True
        elif event.type==pygame.KEYDOWN:
            if not state.mainMenu:
                if event.key==pygame.K_ESCAPE:
                    if state.pauseMenu:
                        resumeGame()
                    else:
                        pauseMenu()
                    blipSound.play()
            if not state.pauseMenu and not state.mainMenu and not state.player.inMove:
                buddons=(pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6)
                if event.key in buddons:
                    o=buddons.index(event.key)
                    if o>2 and state.level.dimension<4 or state.level.dimension==2:
                        continue
                    flipSound.play()
                    state.orient=o
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                for button in state.buttons:
                    if button.hovered:
                        button.function()
                        blipSound.play()
    mouseX,mouseY=pygame.mouse.get_pos()
    for button in state.buttons:
        button.hovered=-10<mouseX-button.x<button.width+10 and -10<mouseY-button.y<button.height+10
    if state.mainMenu:
        screen.fill((0,0,0))
        background1.set_alpha(int(60+40*math.sin(math.pi*t/300)))
        background2.set_alpha(int(60-40*math.sin(math.pi*t/600)))
        background3.set_alpha(int(60+40*math.cos(math.pi*t/300)))
        background4.set_alpha(int(60-40*math.cos(math.pi*t/600)))
        screen.blit(background1,(0,int(t%9500)))
        screen.blit(background2,(0,int(t%9500)))
        screen.blit(background3,(0,int(t%9500)-4500))
        screen.blit(background4,(0,int(t%9500)-4500))
        screen.blit(background1,(0,int(t%9500)-9500))
        screen.blit(background2,(0,int(t%9500)-9500))
        title.set_alpha(min(255,180+90*noise.noise2d(t/200,0)+20*noise.noise2d(t/40,2)+5*noise.noise2d(t/5,6)))
        screen.blit(title,(screenSize/2-411,60))
    else:
        state.player.update(state)
        for n in state.player.getPos():
            if n==-1 or n==state.level.size:
                if state.procedural:
                    state.proceduralLevel+=1
                    generateLevel()
                    state.player.x=1
                    state.player.y=1
                    state.player.z=1
                    state.player.w=1
                else:
                    state.levelNum+=1
                    if state.levelNum>state.maxLevel:
                        state.maxLevel=state.levelNum
                    loadLevel(str(state.levelNum))
                    break
        fg=state.level.foreground
        bg=state.level.background
        newBG=pygame.Color(*bg)
        #hsva=newBG.hsva
        #newBG.hsva=(hsva[0],hsva[1],hsva[0],hsva[3])
        size=state.level.size
        scale=int(screenSize/size)
        halfScale=math.ceil(scale/2)
        scaleSmall=int(screenSize/size*0.9)
        screen.fill(bg)
        pos=state.player.getIntPos()
        for x in range(size):
            for y in range(size):
                deltas=((-1,0),(0,-1),(1,0),(0,1))
                p=orientPos(state.orient,pos,(x,y))
                s=int(state.level[p])
                _fg=[newBG,fg][s]
                _bg=[fg,newBG][s]
                pygame.draw.rect(screen,_bg,(x*scale,y*scale,scale,scale))
                drawCircle(screen,_fg,x*scale+halfScale,y*scale+halfScale,halfScale-1)
                for delta in deltas:
                    dx,dy=delta
                    p=orientPos(state.orient,pos,(x+dx,y+dy))
                    if x+dx<0 or x+dx>=size or y+dy<0 or y+dy>=size or state.level[p]==s:
                        left=x*scale
                        top=y*scale
                        width=scale
                        height=scale
                        if dx:
                            width=math.ceil(width/2)
                        if dy:
                            height=math.ceil(height/2)
                        if dx==1:
                            left+=scale/2
                        if dy==1:
                            top+=scale/2
                        pygame.draw.rect(screen,_fg,(left,top,width,height))
        x,y=flattenPos(state.orient,state.player.getPos())
        drawCircle(screen,(255,0,0),x*scale+scale/2,y*scale+scale/2,scale*0.4)
        pygame.draw.rect(screen,bg,(0,screenSize,screenSize,100))
        text=font1.render(state.level.name,1,fg)
        screen.blit(text,(10,screenSize))
        endPos=state.level.endPos
        text=font2.render("x: %s/%s"%(round(state.player.x),endPos[0]),1,fg)
        screen.blit(text,(screenSize/2+10,screenSize))
        text=font2.render("y: %s/%s"%(round(state.player.y),endPos[1]),1,fg)
        screen.blit(text,(screenSize/2+10,screenSize+25))
        if state.level.dimension>2:
            text=font2.render("z: %s/%s"%(round(state.player.z),endPos[2]),1,fg)
            screen.blit(text,(screenSize/2+10,screenSize+50))
        if state.level.dimension>3:
            text=font2.render("w: %s/%s"%(round(state.player.w),endPos[3]),1,fg)
            screen.blit(text,(screenSize/2+10,screenSize+75))
        pygame.draw.line(screen,bg,(20,20),(20,80),3)
        text=font2.render("xxyxyz"[state.orient],1,bg)
        screen.blit(text,(81,7))
        pygame.draw.line(screen,bg,(20,20),(80,20),3)
        text=font2.render("yzzwww"[state.orient],1,bg)
        screen.blit(text,(16,76))
        if state.pauseMenu:
            surf=pygame.Surface((screenSize,screenSize+100))
            surf.fill((0,0,0))
            surf.set_alpha(200)
            screen.blit(surf,(0,0))
    for button in state.buttons:
        button.render(screen)
    if state.fadeout:
        state.fadeout-=5
        state.image.set_alpha(state.fadeout)
        screen.blit(state.image,(0,0))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
