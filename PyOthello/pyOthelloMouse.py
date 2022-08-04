# Mouse click event functions
finalMousePos = (0,0)
mouseClicked = False

def isMouseClicked()->bool:
    global mouseClicked
    return mouseClicked
def getMousePosition():
    global mouseClicked,finalMousePos
    mouseClicked = False
    return finalMousePos
def getMouseTilePos(mousePosition,CellWidth,CellHeight):
    return (int(mousePosition[0]/CellWidth)-1,int(mousePosition[1]/CellHeight)-2)
def getPosMouseTile(TilePosition,CellWidth,CellHeight):
    return ((TilePosition[0]+1)*CellWidth,(TilePosition[1]+2)*CellHeight)

def tupleTransform(tuple,i,j):
    return (tuple[0]+i,tuple[1]+j)
    
def MouseClicked(mousePos):
    global finalMousePos,mouseClicked
    finalMousePos = mousePos
    mouseClicked = True

