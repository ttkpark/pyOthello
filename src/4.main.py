import pygame
from board import *
from pyOthelloMouse import *

# Board initalization
board = PyOthelloBoard((8,8),0)
drawnboard = PyOthelloBoard((8,8),0)

isGameEnd = False
isPrevPossiblityPlacingNone = False
possible_list = []
def game_white_turn(board:PyOthelloBoard,count):# {True : Completed, False : in-progress}
    if(count==1):
        #initalization of white
        global possible_list,isPrevPossiblityPlacingNone,isGameEnd
        possible_list = specifyPossiblePositions(board,1)#1:white
        
        if(isPrevPossiblityPlacingNone and len(possible_list)==0):
            isGameEnd = True
        isPrevPossiblityPlacingNone = len(possible_list)==0
        if(isPrevPossiblityPlacingNone):
            return True #No Possibility

        for x in possible_list:
            board.setOnBoard(x,2) # highlight

    if(isMouseClicked()):
        print("clicked on white cell")

        pos = getMousePosition()
        panelPos = getMouseTilePos(pos,CellWidth,CellWidth)

        if(panelPos in possible_list):# 둘 수 있는 곳에 두었을 경우
            for x in possible_list:
                board.setOnBoard(x,0) # removing highlight
            for x in specifyCellstoFlip(board,1,panelPos):
                board.setOnBoard(x,1) # flipping to white
            return True
    return False

def game_black_turn(board:PyOthelloBoard,count):# {True : Completed, False : in-progress}
    if(count==1):
        #initalization of black
        global possible_list,isPrevPossiblityPlacingNone,isGameEnd
        possible_list = specifyPossiblePositions(board,-1)#-1:black

        if(isPrevPossiblityPlacingNone and len(possible_list)==0):
            isGameEnd = True
        isPrevPossiblityPlacingNone = len(possible_list)==0
        if(isPrevPossiblityPlacingNone):
            return True #No Possibility

        for x in possible_list:
            board.setOnBoard(x,2) # highlight

    if(isMouseClicked()):
        print("clicked on black cell")
        pos = getMousePosition()
        panelPos = getMouseTilePos(pos,CellWidth,CellWidth)

        if(panelPos in possible_list):# 둘 수 있는 곳에 두었을 경우
            for x in possible_list:
                board.setOnBoard(x,0) # removing highlight
            for x in specifyCellstoFlip(board,-1,panelPos):
                print(x,"flip to black")
                board.setOnBoard(x,-1) # flipping to black
            return True
            
    return False

def main():
    myfont = pygame.font.SysFont(None,int(26*ScreenMultiplier))

    screen = pygame.display.set_mode(ScreenSizeWindow)
    running = True

    background = pygame.image.load("res/background.png")
    background = pygame.transform.scale(background,ScreenSizeWindow)
    header = pygame.image.load("res/header.png")
    header = pygame.transform.scale(header,(320*ScreenMultiplier,61*ScreenMultiplier))
    footer = pygame.image.load("res/footer.png")
    footer = pygame.transform.scale(footer,(320*ScreenMultiplier,32*ScreenMultiplier))
    whiteCell = pygame.image.load("res/white.png")
    whiteCell = pygame.transform.scale(whiteCell,CellSizeWindow)
    whiteCellSmall = pygame.transform.scale(whiteCell,(18*ScreenMultiplier,18*ScreenMultiplier))
    blackCell = pygame.image.load("res/black.png")
    blackCell = pygame.transform.scale(blackCell,CellSizeWindow)
    blackCellSmall = pygame.transform.scale(blackCell,(18*ScreenMultiplier,18*ScreenMultiplier))
    hightlightCell = pygame.image.load("res/hightlight.png")
    hightlightCell = pygame.transform.scale(hightlightCell,CellSizeWindow)
    greenCell = pygame.image.load("res/green.png")
    greenCell = pygame.transform.scale(greenCell,CellSizeWindow)

    round = 0 # 0:black's turn 1:white's turn
    count = 0 # how many loops passed from the start of one's turn? (count==1 : first time.)
    roundcount = 0

    drawnboard.cleanBoard()

    screen.blit(background,(0,0)) # Drawing Background

    #screen.blit(header,(0,0)) # Drawing header
    roundText = ["Black","White"]
    while running:
        count+=1
        res = drawBoard(board,drawnboard,screen,whiteCell,blackCell,hightlightCell,greenCell)
        if(res and not isGameEnd):
            screen.blit(header,(0,0)) # Drawing Background
            screen.blit(footer,(0,320*ScreenMultiplier)) # Drawing Background
            screen.blit(whiteCellSmall,(78*ScreenMultiplier,39*ScreenMultiplier)) # Drawing Small White Cell
            screen.blit(blackCellSmall,(270*ScreenMultiplier,39*ScreenMultiplier)) # Drawing Small Black Cell
            screen.blit(myfont.render(str(board.count(1)),True,(255,255,255)),(36*ScreenMultiplier,40*ScreenMultiplier)) # Drawing White Score
            screen.blit(myfont.render(str(board.count(-1)),True,(255,255,255)),(228*ScreenMultiplier,40*ScreenMultiplier)) # Drawing Black Score
            screen.blit(myfont.render(str("round {}".format(roundcount)),True,(255,255,255)),(132*ScreenMultiplier,40*ScreenMultiplier)) # Drawing Round count
            screen.blit(myfont.render(str("{} Cell Phase.".format(roundText[round])),True,(255,255,255)),(32*ScreenMultiplier,330*ScreenMultiplier))

        elif(isGameEnd):
            screen.blit(header,(0,0)) # Drawing Background
            screen.blit(footer,(0,320*ScreenMultiplier)) # Drawing Background
            screen.blit(whiteCellSmall,(78*ScreenMultiplier,39*ScreenMultiplier)) # Drawing Small White Cell
            screen.blit(blackCellSmall,(270*ScreenMultiplier,39*ScreenMultiplier)) # Drawing Small Black Cell
            screen.blit(myfont.render(str(board.count(1)),True,(255,255,255)),(36*ScreenMultiplier,40*ScreenMultiplier)) # Drawing White Score
            screen.blit(myfont.render(str(board.count(-1)),True,(255,255,255)),(228*ScreenMultiplier,40*ScreenMultiplier)) # Drawing Black Score
            screen.blit(myfont.render(str("game end".format(roundcount)),True,(255,255,255)),(120*ScreenMultiplier,40*ScreenMultiplier)) # Drawing Round count
            screen.blit(myfont.render(str("{} Cell Won.".format(roundText[board.count(1)>board.count(-1)])),True,(255,255,255)),(32*ScreenMultiplier,330*ScreenMultiplier))
            pygame.display.flip()
            

        if(round == 0):#black's turn
            if(game_black_turn(board,count) == True):#if black's turn ends
                round = 1
                roundcount += 1
                count = 0
        elif(round == 1):#white's turn
            if(game_white_turn(board,count) == True):#if white's turn ends
                round = 0
                roundcount += 1
                count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                MouseClicked(pygame.mouse.get_pos())
        

initPygame()
main()
