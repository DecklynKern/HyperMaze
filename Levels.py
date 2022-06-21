from Classes import *
levels={}
parseComma=lambda line:list(map(int,line.split(",")))
for f in os.listdir("levels"):
    if f.endswith(".dat")and f.startswith("level_"):
        id=f[6:-4]
        file=open("levels\\"+f)
        name=file.readline()[:-1]
        dimension=int(file.readline())
        size=int(file.readline())
        endPos=parseComma(file.readline())
        lines=[list(map(int,file.readline()[:-1]))for l in range(size**(dimension-1))]
        fgColour=parseComma(file.readline())
        bgColour=parseComma(file.readline())
        file.close()
        d1=size if dimension>2 else 1
        d2=size if dimension>3 else 1
        layout=[[[]for z in range(d1)]for w in range(d2)]
        for w in range(d2):
            for z in range(d1):
                for y in range(size):
                    layout[w][z].append(lines[w*d1*size+z*size+y])
        final=numpy.transpose(numpy.pad(layout,pad_width=1,mode="constant",constant_values=1))
        levels[id]=Level(name,dimension,final,fgColour,bgColour,endPos)
def loadLevel(name):
    state.level=levels[name]
    state.player=Player(*state.level.startPos)
    state.orient=0
