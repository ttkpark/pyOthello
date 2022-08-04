import pygame
from board import *
from pyOthelloMouse import *
import random

# Board initalization
board = PyOthelloBoard((8,8),0)
drawnboard = PyOthelloBoard((8,8),0)

def CellScoreWeight(position,boardSize):
    maxX = boardSize[0]-1
    maxY = boardSize[1]-1
    good_point_list  = [(0,0),(maxX,maxY),(maxX,0),(0,maxY)]
    bad_point_list   = [(1,0),(1,1),(0,1),
                        (maxX-1,maxY),(maxX-1,maxY-1),(maxX,maxY-1),
                        (maxX-1,0),(maxX-1,1),(maxX,1),
                        (0,maxY-1),(1,maxY),(1,maxY-1)]
    if(position in good_point_list):
        return 1
    elif(position in bad_point_list):
        return -1
    else:
        return 0
def CalculateHeuristic(board:PyOthelloBoard,possible_list,CellValue)->list:
    roundCellVal = [-1,1]
    round = 0
    if(CellValue == 1):
        round = 1
    oppoCellValue = roundCellVal[not round]

    beforeScoreDifference = board.count(CellValue) - board.count(oppoCellValue) 

    if(type(possible_list) != list):
        possible_list = specifyPossiblePositions(board,CellValue)
    
    indexBoards = []
    scoreIndexList = []

    for i in range(len(possible_list)):
        x = possible_list[i]
        nextBoard = board.clone()
        
        for k in possible_list:
            nextBoard.setOnBoard(k,0) # removing highlight
        for k in specifyCellstoFlip(nextBoard,CellValue,x):
            nextBoard.setOnBoard(k,CellValue) # flipping

        new_possible_list = specifyPossiblePositions(nextBoard,oppoCellValue)
        afterScoreDifference = nextBoard.count(CellValue) - nextBoard.count(oppoCellValue)

        nowWeightScore = CellScoreWeight(x,board.boardSize)*4
        nowPossiblityDifference = (len(possible_list) - len(new_possible_list))*2
        nowScoreDifference = int((afterScoreDifference - beforeScoreDifference))

        score = nowWeightScore + nowPossiblityDifference + nowScoreDifference

        indexBoards.append(nextBoard)

        scoreIndexList.append({"i":i,"possiblePosition":x,"score":score,"board":nextBoard})
    return scoreIndexList
def CalculateMiniMax_Heuristic(board:PyOthelloBoard,possible_list,CellValue,goalLevel):
    roundCellVal = [-1,1]
    round = 0
    if(CellValue == 1):
        round = 1
    oppoCellValue = roundCellVal[not round]

    if(goalLevel < 0):
        return None
    scoreIndexList = CalculateHeuristic(board,possible_list,CellValue)

    if(goalLevel < 2):
        return scoreIndexList

    for j in range(len(scoreIndexList)):
        scoreIndexList[j]["i"] = [scoreIndexList[j]["i"]]
        
    #print("\"Level {}\" : {},".format(1,str(scoreIndexList).replace('},','},\n')))

    level = 2
    while(goalLevel>=level):
        scoreIndexList_next = []
        for i in range(len(scoreIndexList)):
            parent = scoreIndexList[i]
            scoreIndexList_next_iter = []

            if(level % 2 == 0):
                possible_list = specifyPossiblePositions(parent["board"],oppoCellValue)
            else:
                possible_list = specifyPossiblePositions(parent["board"],CellValue)

            if(len(possible_list) == 0): # no possible positions -> nothing to do
                parent["i"].append(0)
                scoreIndexList_next.append({"i":parent["i"],"possiblePosition":None,"score":parent["score"],"board":parent["board"]})
                continue
            
            if(level % 2 == 0):
                scoreIndexList_next_iter = CalculateHeuristic(parent["board"],possible_list,oppoCellValue) #Mini
                # in even level, the best one for opponent is chosen.
                
                maxScore = -9999
                best_i = []
                for x in scoreIndexList_next_iter:
                    if(x["score"] > maxScore):
                        maxScore = x["score"]
                        best_i = [x["i"]]
                    elif(x["score"] == maxScore):
                        best_i.append(x["i"])
                
                for i in best_i:
                    new = parent["i"][:]
                    new.append(i)
                    scoreIndexList_next_iter[i]["i"] = new
                    scoreIndexList_next_iter[i]["score"] = parent["score"] - scoreIndexList_next_iter[i]["score"]#Mini            
                    scoreIndexList_next.append(scoreIndexList_next_iter[i])

            else:
                scoreIndexList_next_iter = CalculateHeuristic(parent["board"],possible_list,CellValue)     #Max

                #4.Conversion
                for j in range(len(scoreIndexList_next_iter)):
                    new = parent["i"][:]
                    new.append(j)
                    scoreIndexList_next_iter[j]["i"] = new
                    scoreIndexList_next_iter[j]["score"] += parent["score"] #Max                 
                scoreIndexList_next.extend(scoreIndexList_next_iter)

        scoreIndexList = scoreIndexList_next
        #print("\"Level {}\" : {},".format(level,str(scoreIndexList).replace('},','},\n')))
        level += 1

    print("\"Level {}\" : {},".format(level,str(scoreIndexList).replace('},','},\n')))
    return scoreIndexList

# {True : Completed, False : in-progress}
def game_user_turn(board:PyOthelloBoard,CellValue,count,possible_list,screen=0,myfont=0):
    if(count==1):
        for x in possible_list:
            board.setOnBoard(x,2) # highlight


    if(isMouseClicked()):
        if(len(possible_list)==0):
            return True

        print("clicked on cell {}".format(CellValue))

        pos = getMousePosition()
        panelPos = getMouseTilePos(pos,CellWidth,CellWidth)

        if(panelPos in possible_list):# 둘 수 있는 곳에 두었을 경우
            for x in possible_list:
                board.setOnBoard(x,0) # removing highlight
            for x in specifyCellstoFlip(board,CellValue,panelPos):
                board.setOnBoard(x,CellValue) # flipping
            return True
    return False

def game_HeuristicAI_turn(board:PyOthelloBoard,CellValue,count,possible_list,screen:pygame.Surface,myfont:pygame.font.Font):
    if(count==1):
        #initalization of black
        scoreIndexList = CalculateHeuristic(board,possible_list,CellValue)
        for x in scoreIndexList:
            #print("for possible index {}, {}".format(x[0],x))
            board.setOnBoard(x["possiblePosition"],2) # highlight
            screen.blit(myfont.render(str(x["score"]),True,(0,0,0)),tupleTransform(getPosMouseTile(x["possiblePosition"],CellWidth,CellWidth),CellWidth/4,CellWidth/4)) # Drawing White Score

    if(count == 15000):
    #1if(isMouseClicked()):
        print("Heuristic AI Placing the cell {}".format(CellValue))
        if(len(possible_list)==0):
            return True
            
        scoreIndexList = CalculateHeuristic(board,possible_list,CellValue)
        maxScore = -9999
        maxScoreIndex = []
        for i in range(len(scoreIndexList)):
            if(scoreIndexList[i]["score"] > maxScore):
                maxScore = scoreIndexList[i]["score"]
                maxScoreIndex = [i]
            elif(scoreIndexList[i]["score"] == maxScore):
                maxScoreIndex.append(i)
        
        numIndexes = len(maxScoreIndex)
        randomIndex = maxScoreIndex[random.randint(0,numIndexes-1)]
        panelPos = possible_list[randomIndex]

        if(panelPos in possible_list):# 둘 수 있는 곳에 두었을 경우
            for x in possible_list:
                board.setOnBoard(x,0) # removing highlight
            for x in specifyCellstoFlip(board,CellValue,panelPos):
                print(x,"flip to {}".format(CellValue))
                board.setOnBoard(x,CellValue) # flipping
            return True
    return False

def game_HeuristicMinimaxAI_turn(board:PyOthelloBoard,CellValue,count,possible_list,screen:pygame.Surface,myfont:pygame.font.Font):
    if(count==1):
        #initalization of black
        #scoreIndexList = CalculateMiniMax_Heuristic(board,possible_list,CellValue,3)
        for x in possible_list:
            board.setOnBoard(x,2) # highlight
            #screen.blit(myfont.render(str(x["score"]),True,(0,0,0)),tupleTransform(getPosMouseTile(x["x"],CellWidth,CellWidth),CellWidth/4,CellWidth/4)) # Drawing White Score

    if(count == 15000):
    #if(isMouseClicked()):
        print("Heuristic Minimax AI Placing the cell {}".format(CellValue))
        if(len(possible_list)==0):
            return True

        #panelPos = possible_list[0]
        scoreIndexList = CalculateMiniMax_Heuristic(board,possible_list,CellValue,5)
        print(len(scoreIndexList))
        maxScore = -9999
        maxScoreIndex = []
        for x in scoreIndexList:
            if(x["score"] > maxScore):
                maxScore = x["score"]
                maxScoreIndex = [x["i"]]
            elif(x["score"] == maxScore):
                maxScoreIndex.append(x["i"])
        
        numIndexes = len(maxScoreIndex)
        randomIndex = maxScoreIndex[random.randint(0,numIndexes-1)]

        panelPos = possible_list[0]
        for x in scoreIndexList:
            if(x["i"] == randomIndex):
                panelPos = possible_list[x["i"][0]]
        print(maxScoreIndex)
        print(panelPos)

        if(panelPos in possible_list):# 둘 수 있는 곳에 두었을 경우
            for x in possible_list:
                board.setOnBoard(x,0) # removing highlight
            for x in specifyCellstoFlip(board,CellValue,panelPos):
                print(x,"flip to {}".format(CellValue))
                board.setOnBoard(x,CellValue) # flipping
            return True
    return False

def game_Simple2AI_turn(board:PyOthelloBoard,CellValue,count,possible_list,screen=0,myfont=0):
    if(count==1):
        #initalization of black
        for x in possible_list:
            board.setOnBoard(x,2) # highlight

    if(count == 1):
        print("SimpleAI Placing the cell {}".format(CellValue))
        if(len(possible_list)==0):
            return True

        panelPos = possible_list[-1]
        if(panelPos in possible_list):# 둘 수 있는 곳에 두었을 경우
            for x in possible_list:
                board.setOnBoard(x,0) # removing highlight
            for x in specifyCellstoFlip(board,CellValue,panelPos):
                print(x,"flip to {}".format(CellValue))
                board.setOnBoard(x,CellValue) # flipping
            return True
    return False

def main(Game_mode):
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
    roundCellVal = [-1,1]

    isPrevPossiblityPlacingNone = False
    isGameEnd = False
    possible_list = []

    black_turn_func = game_user_turn
    white_turn_func = game_user_turn

    if Game_mode == 1: # 사람 vs AI
        white_turn_func = game_HeuristicMinimaxAI_turn
    elif Game_mode == 2: # AI vs AI
        black_turn_func = game_HeuristicAI_turn
        white_turn_func = game_HeuristicMinimaxAI_turn
    elif Game_mode != 0:
        print("you are wrong")
        print("We just using Gamemode 0.")
        
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
            
            blackScore = board.count(-1)
            whiteScore = board.count(1)
            if(blackScore > whiteScore):
                screen.blit(myfont.render("{} Cell Won.".format(roundText[0]),True,(255,255,255)),(32*ScreenMultiplier,330*ScreenMultiplier))
            elif(blackScore < whiteScore):
                screen.blit(myfont.render("{} Cell Won.".format(roundText[1]),True,(255,255,255)),(32*ScreenMultiplier,330*ScreenMultiplier))
            else:
                screen.blit(myfont.render("no one Won.",True,(255,255,255)),(32*ScreenMultiplier,330*ScreenMultiplier))
            pygame.display.flip()


        if(count == 1): #Turn initialization
            possible_list = specifyPossiblePositions(board,roundCellVal[round])
            if(isPrevPossiblityPlacingNone and len(possible_list)==0):
                isGameEnd = True
            isPrevPossiblityPlacingNone = len(possible_list)==0

        if(round == 0):#black's turn
            if(black_turn_func(board,roundCellVal[round],count,possible_list,screen,myfont) == True):#if black's turn ends
                round = 1
                roundcount += 1
                count = 0
        elif(round == 1):#white's turn
            if(white_turn_func(board,roundCellVal[round],count,possible_list,screen,myfont) == True):#if white's turn ends
                round = 0
                roundcount += 1
                count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                MouseClicked(pygame.mouse.get_pos())

Game_mode = int(input("어떤 게임모드로 하고 싶으십니까? : 0=사람vs사람 1=사람vsAI 2=AIvsAI > "))
initPygame()
main(Game_mode)
