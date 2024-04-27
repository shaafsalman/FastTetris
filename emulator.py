import pygame
import sys
from game import Game
from colors import Colors
from Base_Emulator import TetrisBase


class Human_Emulator(TetrisBase):

    # self down
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.game.game_over:
                    self.game.game_over = False
                    self.game.reset()
                    if self.game.score > self.highest_score:
                        self.highest_score = self.game.score
                if not self.game.game_over:
                    if event.key == pygame.K_LEFT:
                        self.game.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.game.move_right()
                    elif event.key == pygame.K_DOWN:
                        self.game.move_down()
                        self.game.update_score(0, 1)
                    elif event.key == pygame.K_UP:
                        self.game.rotate()

            # if event.type == self.GAME_UPDATE and not self.game.game_over:
            #     self.game.move_down()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_rect.collidepoint(mouse_pos):
                    return True  # Indicates Back button click

        return False  # No Back button click

    def run_game(self):
        while True:
            if self.handle_events():
                break
            self.render()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Human_Emulator()
    while True:
        game.run_game()
