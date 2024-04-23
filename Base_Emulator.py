import pygame
import sys
from game import Game
from colors import Colors
from agent import Agent

class TetrisBase:
    def __init__(self):
        pygame.init()
        self.title_font = pygame.font.Font(None, 40)
        self.score_font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 28)
        self.score_surface = self.title_font.render("Score", True, Colors.white)
        self.lines_surface = self.title_font.render("Number of Lines", True, Colors.white)
        self.next_surface = self.title_font.render("Next", True, Colors.white)
        self.game_over_surface = self.title_font.render("GAME OVER", True, Colors.white)
        self.highest_score_surface = self.title_font.render("Highest Score: ", True, Colors.white)
        self.agent_surface = self.title_font.render("Agent: ", True, Colors.white)
        self.back_surface = self.button_font.render("Back", True, Colors.white)
        self.score_rect = pygame.Rect(320, 20, 200, 40)
        self.lines_rect = pygame.Rect(520, 20, 250, 40)
        self.next_rect = pygame.Rect(320, 215, 200, 40)
        self.game_over_rect = pygame.Rect(320, 450, 300, 40)
        self.agent_rect = pygame.Rect(20, 70, 200, 40)
        self.back_rect = pygame.Rect(890, 10, 100, 50)
        self.screen_width = 1000
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Fast Tetris")
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.agent = Agent()
        self.GAME_UPDATE = pygame.USEREVENT
        self.highest_score = self.game.highest_score
        pygame.time.set_timer(self.GAME_UPDATE, 200)

    def render(self):
        self.screen.fill(Colors.BACKGROUND_COLOR)

        self.screen.blit(self.score_surface, (320, 20))
        score_value_surface = self.score_font.render(str(self.game.score), True, Colors.white)
        self.screen.blit(score_value_surface, (320, 55))

        self.screen.blit(self.lines_surface, (520, 20))
        lines_value_surface = self.score_font.render(str(self.game.lines), True, Colors.white)
        self.screen.blit(lines_value_surface, (520, 55))

        self.screen.blit(self.next_surface, (320, 215))
        next_shape_preview_position = (320, 250)

        highest_score_text_rect = self.highest_score_surface.get_rect(
            midtop=(next_shape_preview_position[0] + 100, next_shape_preview_position[1] + 240))
        self.screen.blit(self.highest_score_surface, highest_score_text_rect)
        highest_score_value_surface = self.score_font.render(str(self.highest_score), True, Colors.white)
        highest_score_value_rect = highest_score_value_surface.get_rect(
            midtop=(next_shape_preview_position[0] + 300, next_shape_preview_position[1] + 240))
        self.screen.blit(highest_score_value_surface, highest_score_value_rect)

        agent_text_rect = self.agent_surface.get_rect(
            midtop=(next_shape_preview_position[0] + 100, next_shape_preview_position[1] + 290))
        self.screen.blit(self.agent_surface, agent_text_rect)

        agent_type_surface = self.score_font.render(self.agent.agent_type, True, Colors.white)
        agent_type_rect = agent_type_surface.get_rect(
            midtop=(next_shape_preview_position[0] + 300, next_shape_preview_position[1] + 290))
        self.screen.blit(agent_type_surface, agent_type_rect)

        back_color = Colors.light_blue
        pygame.draw.rect(self.screen, back_color, self.back_rect, border_radius=10)
        pygame.draw.rect(self.screen, Colors.dark_blue, self.back_rect, width=4, border_radius=10)
        self.screen.blit(self.back_surface, self.back_surface.get_rect(center=self.back_rect.center))

        if self.game.game_over:
            self.screen.blit(self.game_over_surface, (320, 450))

        self.game.draw(self.screen)
        pygame.display.update()
