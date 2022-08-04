import pygame
# main functions
def initPygame():
    pygame.init()
    logo = pygame.image.load("res/icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("pyOthello")

def main():
    screen = pygame.display.set_mode((320,352))
    running = True
    background = pygame.image.load("res/background.png")
    whiteCell = pygame.image.load("res/white.png")
    blackCell = pygame.image.load("res/black.png")
    while running:
        screen.blit(background,(0,0))
        screen.blit(whiteCell,(32,64))
        screen.blit(blackCell,(64,64))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

initPygame()
main()