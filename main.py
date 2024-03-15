import sys

import pygame

from grid import Grid
from all_blocks import *

pygame.init()

screen = pygame.display.set_mode((300, 600))

pygame.display.set_caption("FastTetris")
clock = pygame.time.Clock()
game_grid = Grid()
game_grid.print_grid()

dark_blue = (44, 44, 127)
block = LBlock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(dark_blue)
    game_grid.draw(screen)
    block.draw(screen)

    pygame.display.update()
    clock.tick(60)
