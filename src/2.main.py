import pygame

ScreenMultiplier = 2
CellWidth = 32*ScreenMultiplier
CellSizeWindow = (CellWidth,CellWidth)
ScreenSizeWindow = (10*CellWidth,11*CellWidth)

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

# main functions
def initPygame():
    pygame.init()
    logo = pygame.image.load("res/icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("pyOthello")

def drawCell(screen,cell,pos):
    screen.blit(cell,((pos[0]+1)*CellWidth,(pos[1]+2)*CellWidth))


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

    round = 0
    updated = False

    screen.blit(background,(0,0))

    while running:

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
            updated = False
                
        #drawCell(screen,whiteCell,(0,0))
        #drawCell(screen,blackCell,(1,0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                panelPos = (int(pos[0]/CellWidth)-1,int(pos[1]/CellWidth)-2)
                if(0<=panelPos[0]<8 and 0<=panelPos[1]<8):
                    print(pos)
                    print(panelPos)
                    if(board[panelPos[0]][panelPos[1]] == 0):
                        if(round % 2 == 0):
                            board[panelPos[0]][panelPos[1]] = -1
                        else:
                            board[panelPos[0]][panelPos[1]] = 1
                        round = round+1
                        print(board)


initBoard()
initPygame()
main()