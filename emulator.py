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
        self.score_rect = pygame.Rect(320, 55, 170, 60)
        self.next_rect = pygame.Rect(320, 215, 170, 180)
        self.screen = pygame.display.set_mode((1300, 700))
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
        self.screen.blit(self.score_surface, self.score_rect)
        self.screen.blit(self.next_surface, self.next_rect)
        if self.game.game_over:
            self.screen.blit(self.game_over_surface, (320, 450))
        pygame.draw.rect(self.screen, Colors.light_blue, self.score_rect, 0, 10)
        self.screen.blit(score_value_surface, score_value_surface.get_rect(center=self.score_rect.center))
        pygame.draw.rect(self.screen, Colors.light_blue, self.next_rect, 0, 10)
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
