import pygame,sys
import pygame.time

import game
from game import Game
from colors import Colors



pygame.init()

screen = pygame.display.set_mode((300, 600))

pygame.display.set_caption("FastTetris")
clock = pygame.time.Clock()

dark_blue = (44, 44, 127)


GAME_UPDATE =  pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()


    game.draw(screen)

    pygame.display.update()
    clock.tick(60)
