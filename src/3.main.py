import pygame
from sympy import re

# Screen constants
ScreenMultiplier = 2
CellWidth = 32*ScreenMultiplier
CellSizeWindow = (CellWidth,CellWidth)
ScreenSizeWindow = (10*CellWidth,11*CellWidth)

# Board initalization
boardSize = (8,8)
board = []
drawnboard = []
for i in range(boardSize[1]):
    board += [[0]*boardSize[0]]
    drawnboard += [[0]*boardSize[0]]
# 0 : no cell is placed
# 1 : white cell
#-1 : black cell
# 2 : white circle point(highlight of AI)
def initBoard():
    ## cell layout
    board[3][3] = 1
    board[3][4] = -1
    board[4][3] = -1
    board[4][4] = 1


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
def getMouseTilePos(mousePosition):
    return (int(mousePosition[0]/CellWidth)-1,int(mousePosition[1]/CellWidth)-2)


# main functions
def initPygame():
    pygame.init()
    logo = pygame.image.load("res/icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("pyOthello")

def drawCell(screen,cell,pos):
    screen.blit(cell,((pos[0]+1)*CellWidth,(pos[1]+2)*CellWidth))

def drawBoard(board,screen,whiteCell,blackCell,hightlightCell,greenCell):
    updated = False
    for i in range(boardSize[0]):
        for j in range(boardSize[1]):
            if(drawnboard[i][j] != board[i][j]):
                if(board[i][j] == 2):
                    drawCell(screen,hightlightCell,(i,j))
                    print("hightlight on {}".format((i,j)))
                elif(board[i][j] == 1):
                    drawCell(screen,whiteCell,(i,j))
                    print("while on {}".format((i,j)))
                elif(board[i][j] == 0):
                    drawCell(screen,greenCell,(i,j))
                    print("green on {}".format((i,j)))
                elif(board[i][j] == -1):
                    drawCell(screen,blackCell,(i,j))
                    print("black on {}".format((i,j)))
                drawnboard[i][j] = board[i][j]
                updated = True
        
    if(updated):
        pygame.display.flip()

# 이곳에 돌을 놓을 수 있는 곳을 모두 알아내는 함수.
def specifyPossiblePositions(board,cellValue):
    possiblelist = []
    for i in range(boardSize[0]):
        for j in range(boardSize[1]):
            if(isPossiblePositiontoPlace(board,cellValue,(i,j))):
                possiblelist.append((i,j))
    return possiblelist
# board 위에 position 위치에 cellValue 의 돌을 놓을 수 있는지 확인하는 함수.
def isPossiblePositiontoPlace(board,cellValue,position):
    # 상대방의 돌을 감싸면서 둘 수만 있다.
    # 상하좌우 대각선 8방향으로 자신돌 - 상대방돌 x N - 자신돌의 패턴인지 검사한다.
    # 커서가 한 방향으로 움직이면서 검사한다면
        # 0:자신돌, 1~n:상대돌, n+1:자신돌 의 패턴이다.
    
    cell = board[position[0]][position[1]]
    if(cell == -1 or cell == 1):
        #print(position ,"not possible : already placed")
        return False

    isAloneCell = True
    for i in range(9):
        fcx = position[0]+int(i/3)-1
        fcy = position[1]+int(i%3)-1
        if(0<=fcx<boardSize[0] and 0<=fcy<boardSize[1]):
            cell = board[fcx][fcy]
            if(cell == 1 or cell == -1):
                isAloneCell = False
                break
    if(isAloneCell):
        return False


    cursorx = position[0]
    cursory = position[1]
    cell = board[cursorx][cursory]

    oppCellValue = -cellValue

    directions = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)] # 8방위
    for direction in directions:
        cursorx = position[0] + direction[0]
        cursory = position[1] + direction[1]
        phase = 1
        while (0<=cursorx<boardSize[0] and 0<=cursory<boardSize[1]):
            prevCell = cell
            cell = board[cursorx][cursory]
            
            if(phase == 1):
                if(cell != oppCellValue):
                    #print(position ,"not possible : dir,pos=",direction,(cursorx,cursory),"no starting opposite")
                    break
            else:
                if (cell != -1 and cell != 1):
                    break
                elif(prevCell == cellValue):
                    #print(position ,"not possible : dir,pos=",direction,(cursorx,cursory),"prev is mine")
                    break

                #prev is yours and now is mine  : Correct. return True
                elif(cell == cellValue):
                    return True

                #prev is yours and now is yours : Keep going!
                #else:

            phase+=1
            cursorx += direction[0]
            cursory += direction[1]
        #if(not (0<=cursorx<boardSize[0] and 0<=cursory<boardSize[1])):
            #print(position ,"not possible : dir,pos=",direction,(cursorx,cursory),"index out of range")
            
            
    #print(position ,"not possible : no linings")
    return False # array out of bounds
# board 위에 position 위치에 cellValue의 돌을 놓을 경우 뒤집히는 돌들의 위치를 모두 알아내는 함수
def specifyCellstoFlip(board,cellValue,position):
    celllist = []
    cursorx = position[0]
    cursory = position[1]
    cell = board[cursorx][cursory]

    oppCellValue = -cellValue

    for direction in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]: # 8방위:
        cursorx = position[0] + direction[0]
        cursory = position[1] + direction[1]
        phase = 1
        while (0<=cursorx<boardSize[0] and 0<=cursory<boardSize[1]):
            prevCell = cell
            cell = board[cursorx][cursory]
            
            if(phase == 1):
                if(cell != oppCellValue):
                    #print(position ,"not possible : dir,pos=",direction,(cursorx,cursory),"no starting opposite")
                    break
            else:
                if (cell != -1 and cell != 1):
                    break
                elif (prevCell == cellValue):
                    #print(position ,"not possible : dir,pos=",direction,(cursorx,cursory),"prev is mine")
                    break
                elif(cell == cellValue):
                    #print(position ,"possible : dir,pos=",direction,(cursorx,cursory),"start adding")
                    for i in range(phase):
                        #print("adding cell",(cursorx-direction[0]*(i+1),cursory-direction[1]*(i+1)))
                        celllist.append((cursorx-direction[0]*(i+1),cursory-direction[1]*(i+1)))
                    break

            phase+=1
            cursorx += direction[0]
            cursory += direction[1]

    return celllist


possible_list = []
def game_white_turn(board,count):# {True : Completed, False : in-progress}
    if(count==1):
        #initalization of black
        global possible_list
        possible_list = specifyPossiblePositions(board,1)#-1:white
        for x in possible_list:
            board[x[0]][x[1]] = 2 # highlight

    if(isMouseClicked()):
        print("clicked on black cell")
        pos = getMousePosition()
        panelPos = getMouseTilePos(pos)

        if(panelPos in possible_list):# 둘 수 있는 곳에 두었을 경우
            for x in possible_list:
                board[x[0]][x[1]] = 0 # removing highlight
            for x in specifyCellstoFlip(board,1,panelPos):
                board[x[0]][x[1]] = 1 # flipping to white
            return True
    return False

def game_black_turn(board,count):# {True : Completed, False : in-progress}
    if(count==1):
        #initalization of black
        global possible_list
        possible_list = specifyPossiblePositions(board,-1)#-1:black
        for x in possible_list:
            board[x[0]][x[1]] = 2 # highlight

    if(isMouseClicked()):
        print("clicked on black cell")
        pos = getMousePosition()
        panelPos = getMouseTilePos(pos)

        if(panelPos in possible_list):# 둘 수 있는 곳에 두었을 경우
            for x in possible_list:
                board[x[0]][x[1]] = 0 # removing highlight
            for x in specifyCellstoFlip(board,-1,panelPos):
                print(x,"flip to black")
                board[x[0]][x[1]] = -1 # flipping to black
            return True
            
    return False

def main():
    screen = pygame.display.set_mode(ScreenSizeWindow)
    running = True

    background = pygame.image.load("res/background.png")
    background = pygame.transform.scale(background,ScreenSizeWindow)
    whiteCell = pygame.image.load("res/white.png")
    whiteCell = pygame.transform.scale(whiteCell,CellSizeWindow)
    blackCell = pygame.image.load("res/black.png")
    blackCell = pygame.transform.scale(blackCell,CellSizeWindow)
    hightlightCell = pygame.image.load("res/hightlight.png")
    hightlightCell = pygame.transform.scale(hightlightCell,CellSizeWindow)
    greenCell = pygame.image.load("res/green.png")
    greenCell = pygame.transform.scale(greenCell,CellSizeWindow)

    round = 0 # 0:black's turn 1:white's turn
    count = 0 # how many loops passed from the start of one's turn? (count==1 : first time.)

    screen.blit(background,(0,0)) # Drawing Background

    while running:
        count+=1
        drawBoard(board,screen,whiteCell,blackCell,hightlightCell,greenCell)

        if(round == 0):#black's turn
            if(game_black_turn(board,count) == True):#if black's turn ends
                round = 1
                count = 0
        elif(round == 1):#white's turn
            if(game_white_turn(board,count) == True):#if white's turn ends
                round = 0
                count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                global finalMousePos,mouseClicked
                finalMousePos = pygame.mouse.get_pos()
                mouseClicked = True
        

initBoard()
initPygame()
main()
