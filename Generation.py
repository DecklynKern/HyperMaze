from Levels import *
def generateLevel():
    n=state.proceduralLevel
    minDim=3*math.tanh(n/6)**2+1
    maxDim=2#3.1*math.tanh(n/15)+1.5
    diff=maxDim-minDim
    dim=min(4,minDim+diff*random.random())
    size=int(5*n**.6/dim**2)*2+1
    dim=math.ceil(dim)
    dimMap=[1 if dim>n else 0 for n in range(4)]
    array=numpy.ones([size if dimMap[n]else 1 for n in range(4)])
    changes={
        0:(1,0,0,0),
        1:(-1,0,0,0),
        2:(0,1,0,0),
        3:(0,-1,0,0),
        4:(0,0,1,0),
        5:(0,0,-1,0),
        6:(0,0,0,1),
        7:(0,0,0,-1),
    }
    def recurse(point):
        deltas=list(range(2*dim))
        random.shuffle(deltas)
        for c in deltas:
            change=changes[c]
            index1=tuple(point[n]+change[n]for n in range(4))
            index2=tuple(point[n]+2*change[n]for n in range(4))
            for n in range(4):
                if index1[n]<0 or index1[n]>=size:
                    break
            else:
                if array[index2]:
                    array[index1]=0
                    array[index2]=0
                    recurse(index2)
    recurse(tuple(2*random.randrange(size//2) if dimMap[n]else 0 for n in range(4)))
    fg=pygame.Color(*(random.randrange(256)for n in range(3)))
    hsva=fg.hsva
    c=((hsva[0]+random.randrange(-15,16)+180)%360,hsva[1],100-hsva[2],100,)
    bg=pygame.Color(0,0,0)
    bg.hsva=c
    endPos=[size+1]+[2*(random.randrange(size)//2)+1 for n in range(dim-1)]
    random.shuffle(endPos)
    endPos+=[1 for n in range(4-dim)]
    array=numpy.pad(array,pad_width=1,mode="constant",constant_values=1)
    state.level=Level("Level %s"%n,dim,array,fg,bg,endPos)
