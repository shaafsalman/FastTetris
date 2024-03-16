import pygame
import sys
from game import Game
from colors import Colors
from agent import Agent

game_speed = 100


class TetrisGame:
    def __init__(self):
        pygame.init()

        # Fonts
        self.title_font = pygame.font.Font(None, 40)
        self.score_font = pygame.font.Font(None, 30)

        # Text surfaces
        self.score_surface = self.title_font.render("Score", True, Colors.white)
        self.lines_surface = self.title_font.render("Number of Lines", True, Colors.white)
        self.next_surface = self.title_font.render("Next", True, Colors.white)
        self.game_over_surface = self.title_font.render("GAME OVER", True, Colors.white)
        self.highest_score_surface = self.title_font.render("Highest Score: ", True, Colors.white)
        self.agent_surface = self.title_font.render("Agent: ", True, Colors.white)

        # Rectangles
        self.score_rect = pygame.Rect(1200, 55, 170, 60)
        self.lines_rect = pygame.Rect(1200, 55, 170, 60)
        self.next_rect = pygame.Rect(1200, 215, 170, 180)
        self.highest_score_rect = pygame.Rect(20, 20, 200, 40)
        self.agent_rect = pygame.Rect(20, 70, 200, 40)

        # Screen setup
        self.screen_width, self.screen_height = 1300, 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Fast Tetris")

        # Clock
        self.clock = pygame.time.Clock()

        # Game setup
        self.game = Game()
        self.GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.GAME_UPDATE, game_speed)

        # Initialize the highest score and agent type
        self.highest_score = self.game.highest_score
        self.agent_type = "AI"

        self.agent = Agent()

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
                    #self.game.update_score(0, 1)
                elif move == "ROTATE":
                    self.game.rotate()

    def render(self):
        self.screen.fill(Colors.BACKGROUND_COLOR)

        # Draw score
        self.screen.blit(self.score_surface, (320, 20))
        score_value_surface = self.score_font.render(str(self.game.score), True, Colors.white)
        self.screen.blit(score_value_surface, (320, 55))

        # Draw number of lines
        self.screen.blit(self.lines_surface, (520, 20))
        lines_value_surface = self.score_font.render(str(self.game.lines), True, Colors.white)
        self.screen.blit(lines_value_surface, (520, 55))

        # Draw next shape
        self.screen.blit(self.next_surface, (320, 215))
        next_shape_preview_position = (320, 250)
        if hasattr(self.game, 'next_shape') and self.game.next_shape is not None:
            for y, row in enumerate(self.game.next_shape.matrix):
                for x, block in enumerate(row):
                    if block:
                        pygame.draw.rect(self.screen, Colors.light_blue,
                                         pygame.Rect(next_shape_preview_position[0] + x * 20,
                                                     next_shape_preview_position[1] + y * 20, 20, 20))

        # Draw highest score below next shape
        highest_score_text_rect = self.highest_score_surface.get_rect(
            midtop=(next_shape_preview_position[0] + 100, next_shape_preview_position[1] + 240))
        self.screen.blit(self.highest_score_surface, highest_score_text_rect)

        highest_score_value_surface = self.score_font.render(str(self.highest_score), True, Colors.white)
        highest_score_value_rect = highest_score_value_surface.get_rect(
            midtop=(next_shape_preview_position[0] + 300, next_shape_preview_position[1] + 240))
        self.screen.blit(highest_score_value_surface, highest_score_value_rect)

        # Draw agent type below highest score
        agent_text_rect = self.agent_surface.get_rect(
            midtop=(next_shape_preview_position[0] + 100, next_shape_preview_position[1] + 290))
        self.screen.blit(self.agent_surface, agent_text_rect)

        agent_type_surface = self.score_font.render(self.agent_type, True, Colors.white)
        agent_type_rect = agent_type_surface.get_rect(
            midtop=(next_shape_preview_position[0] + 300, next_shape_preview_position[1] + 290))
        self.screen.blit(agent_type_surface, agent_type_rect)

        # Draw game over message if applicable
        if self.game.game_over:
            self.screen.blit(self.game_over_surface, (320, 450))

        self.game.draw(self.screen)  # Draw the game grid and blocks
        pygame.display.update()

    def run_game(self):
        while True:
            self.handle_events()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    tetris_game = TetrisGame()
    tetris_game.run_game()
