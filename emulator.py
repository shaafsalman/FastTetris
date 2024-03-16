import pygame
import sys
from game import Game
from colors import Colors


class TetrisGame:
    def __init__(self):
        pygame.init()
        self.title_font = pygame.font.Font(None, 40)
        self.score_surface = self.title_font.render("Score", True, Colors.white)
        self.next_surface = self.title_font.render("Next", True, Colors.white)
        self.game_over_surface = self.title_font.render("GAME OVER", True, Colors.white)
        self.score_rect = pygame.Rect(1200, 55, 170, 60)
        self.next_rect = pygame.Rect(1200, 215, 170, 180)
        self.screen_width = 1300
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Fast Tetris")
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.GAME_UPDATE, 200)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.game.game_over:
                    self.game.game_over = False
                    self.game.reset()
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
            if event.type == self.GAME_UPDATE and not self.game.game_over:
                self.game.move_down()

    def render(self):
        score_value_surface = self.title_font.render(str(self.game.score), True, Colors.white)
        self.screen.fill(Colors.dark_blue)
        self.screen.blit(self.score_surface, (320, 20))  # Adjust as necessary
        self.screen.blit(score_value_surface, (320, 55))  # Adjust as necessary
        self.screen.blit(self.next_surface, (320, 215))  # Adjust as necessary

        # Assuming self.game.next_shape returns a shape object with a method to draw itself or a matrix of its structure
        next_shape_preview_position = (320, 250)  # Adjust starting position as necessary
        if hasattr(self.game, 'next_shape') and self.game.next_shape is not None:
            # This is a placeholder for drawing the next shape, adjust according to your game's implementation
            for y, row in enumerate(self.game.next_shape.matrix):  # Assuming the shape has a 'matrix' attribute
                for x, block in enumerate(row):
                    if block:  # Assuming a nonzero value indicates a block
                        pygame.draw.rect(self.screen, Colors.light_blue,
                                         pygame.Rect(next_shape_preview_position[0] + x * 20,
                                                     next_shape_preview_position[1] + y * 20, 20, 20))

        if self.game.game_over:
            self.screen.blit(self.game_over_surface, (320, 450))
        self.game.draw(self.screen)
        pygame.display.update()

    def run_game(self):
        while True:
            self.handle_events()
            self.render()
            self.clock.tick(60)


if __name__ == "__main__":
    tetris_game = TetrisGame()
    tetris_game.run_game()
