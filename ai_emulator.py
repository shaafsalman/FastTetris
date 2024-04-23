import sys
import pygame

from Base_Emulator import TetrisBase


class AI_Emulator(TetrisBase):

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.GAME_UPDATE and not self.game.game_over:
                move = self.agent.make_move()
                if move == "LEFT":
                    self.game.move_left()
                elif move == "RIGHT":
                    self.game.move_right()
                elif move == "DOWN":
                    self.game.move_down()
                    self.game.update_score(0, 1)
                elif move == "ROTATE":
                    self.game.rotate()

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
    game = AI_Emulator()
    while True:
        game.run_game()
