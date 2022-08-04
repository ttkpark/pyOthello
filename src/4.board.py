import pygame


# Screen constants
ScreenMultiplier = 1.8
CellWidth = 32*ScreenMultiplier
CellSizeWindow = (CellWidth,CellWidth)
ScreenSizeWindow = (10*CellWidth,11*CellWidth)

# 0 : no cell is placed
# 1 : white cell
#-1 : black cell
# 2 : white circle point(highlight of AI)
class PyOthelloBoard:
    boardSize = tuple()
    board = []

    def __init__(self,boardSize,initval=0):
        self.boardSize = boardSize
        self.cleanBoard(initval)
        self.initBoard(initval)
    
    def initBoard(self,initval=0):
        ## cell layout
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1
    def cleanBoard(self,initval=0):
        self.board = []
        for i in range(self.boardSize[1]):
            self.board += [[initval]*self.boardSize[0]]

    def setOnBoard(self,position,cellValue):
        self.board[position[0]][position[1]] = cellValue
    def getOnBoard(self,position):
        return self.board[position[0]][position[1]]

    def count(self,CellValue):
        count = 0
        for list in self.board:
            count += list.count(CellValue)
        return count
        

    def __list__(self):
        return self.board

# window functions
def initPygame():
    pygame.init()
    logo = pygame.image.load("res/icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("pyOthello")

def drawCell(screen,cell,pos):
    screen.blit(cell,((pos[0]+1)*CellWidth,(pos[1]+2)*CellWidth))

def drawBoard(board:PyOthelloBoard,drawnboard:PyOthelloBoard,screen,whiteCell,blackCell,hightlightCell,greenCell):
    updated = False
    for i in range(board.boardSize[0]):
        for j in range(board.boardSize[1]):
            if(drawnboard.getOnBoard((i,j)) != board.getOnBoard((i,j))):
                if(board.getOnBoard((i,j)) == 2):
                    drawCell(screen,hightlightCell,(i,j))
                    print("hightlight on {}".format((i,j)))
                elif(board.getOnBoard((i,j)) == 1):
                    drawCell(screen,whiteCell,(i,j))
                    print("while on {}".format((i,j)))
                elif(board.getOnBoard((i,j)) == 0):
                    drawCell(screen,greenCell,(i,j))
                    print("green on {}".format((i,j)))
                elif(board.getOnBoard((i,j)) == -1):
                    drawCell(screen,blackCell,(i,j))
                    print("black on {}".format((i,j)))
                drawnboard.setOnBoard((i,j),board.getOnBoard((i,j)))
                updated = True
        
    if(updated):
        pygame.display.flip()
        return True
    else:
        return False



# 이곳에 돌을 놓을 수 있는 곳을 모두 알아내는 함수.
def specifyPossiblePositions(board:PyOthelloBoard,cellValue):
    possiblelist = []
    for i in range(board.boardSize[0]):
        for j in range(board.boardSize[1]):
            if(isPossiblePositiontoPlace(board,cellValue,(i,j))):
                possiblelist.append((i,j))
    return possiblelist
# board 위에 position 위치에 cellValue 의 돌을 놓을 수 있는지 확인하는 함수.
def isPossiblePositiontoPlace(board:PyOthelloBoard,cellValue,position):
    # 상대방의 돌을 감싸면서 둘 수만 있다.
    # 상하좌우 대각선 8방향으로 자신돌 - 상대방돌 x N - 자신돌의 패턴인지 검사한다.
    # 커서가 한 방향으로 움직이면서 검사한다면
        # 0:자신돌, 1~n:상대돌, n+1:자신돌 의 패턴이다.
    
    cell = board.getOnBoard(position)
    if(cell == -1 or cell == 1):
        #print(position ,"not possible : already placed")
        return False

    isAloneCell = True
    for i in range(9):
        fcx = position[0]+int(i/3)-1
        fcy = position[1]+int(i%3)-1
        if(0<=fcx<board.boardSize[0] and 0<=fcy<board.boardSize[1]):
            cell = board.getOnBoard((fcx,fcy))
            if(cell == 1 or cell == -1):
                isAloneCell = False
                break
    if(isAloneCell):
        return False


    cursorx = position[0]
    cursory = position[1]
    cell = board.getOnBoard((cursorx,cursory))

    oppCellValue = -cellValue

    directions = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)] # 8방위
    for direction in directions:
        cursorx = position[0] + direction[0]
        cursory = position[1] + direction[1]
        phase = 1
        while (0<=cursorx<board.boardSize[0] and 0<=cursory<board.boardSize[1]):
            prevCell = cell
            cell = board.getOnBoard((cursorx,cursory))
            
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
def specifyCellstoFlip(board:PyOthelloBoard,cellValue,position):
    celllist = []
    cursorx = position[0]
    cursory = position[1]
    cell = board.getOnBoard((cursorx,cursory))

    oppCellValue = -cellValue

    for direction in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]: # 8방위:
        cursorx = position[0] + direction[0]
        cursory = position[1] + direction[1]
        phase = 1
        while (0<=cursorx<board.boardSize[0] and 0<=cursory<board.boardSize[1]):
            prevCell = cell
            cell = board.getOnBoard((cursorx,cursory))
            
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
