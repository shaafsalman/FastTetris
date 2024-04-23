import pygame
import sys
from game import Game
from colors import Colors
from agent import Agent

class AITetrisGame:
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
        # self.agent_type = Agent()  # Create an instance of the Agent class
        self.GAME_UPDATE = pygame.USEREVENT
        self.highest_score = self.game.highest_score
        pygame.time.set_timer(self.GAME_UPDATE, 200)

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

        agent_type_surface = self.score_font.render(self.agent.agent_type, True, Colors.white)
        agent_type_rect = agent_type_surface.get_rect(
            midtop=(next_shape_preview_position[0] + 300, next_shape_preview_position[1] + 290))
        self.screen.blit(agent_type_surface, agent_type_rect)

        # Draw back button
        back_color = Colors.light_blue
        pygame.draw.rect(self.screen, back_color, self.back_rect, border_radius=10)
        pygame.draw.rect(self.screen, Colors.dark_blue, self.back_rect, width=4, border_radius=10)
        self.screen.blit(self.back_surface, self.back_surface.get_rect(center=self.back_rect.center))

        # Draw game over message if applicable
        if self.game.game_over:
            self.screen.blit(self.game_over_surface, (320, 450))

        self.game.draw(self.screen)  # Draw the game grid and blocks
        pygame.display.update()

    def run_game(self):
        while True:
            if self.handle_events():  # Check for Back button click
                break  # Exit the loop if Back button is clicked
            self.render()
            self.clock.tick(60)

if __name__ == "__main__":
    game = AITetrisGame()
    while True:
        game.run_game()
        # After the game loop exits, create a new instance for a new game
        # game = AITetrisGame()