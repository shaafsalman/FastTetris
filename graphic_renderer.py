import pygame
from FastTetris.colors import Colors

class Renderer:
    def __init__(self):
        """Initialize the Renderer."""
        pygame.init()
        self.title_font = pygame.font.Font(None, 40)
        self.score_font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 28)
        self.score_surface = self.title_font.render("Score", True, Colors.white)
        self.high_score_surface = self.title_font.render("High Score:", True, Colors.white)
        self.back_surface = self.button_font.render("Back", True, Colors.white)
        self.lines_surface = self.title_font.render("Number of Lines", True, Colors.white)
        self.next_shape_surface = self.title_font.render("Next Shape", True, Colors.white)
        self.current_shape_surface = self.title_font.render("Current Shape", True, Colors.white)
        self.game_over_surface = self.title_font.render("GAME OVER", True, Colors.white)
        self.generation_surface = self.title_font.render("Generation:", True, Colors.white)
        self.agent_surface = self.title_font.render("Agent:", True, Colors.white)
        self.player_weights_surface = self.title_font.render("Player ", True, Colors.white)
        self.screen_width = 1000
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Fast Tetris")

        # Define the vertical spacing between elements
        self.vertical_spacing = 120

        # Define the horizontal positions for all elements
        self.score_x = 320
        self.high_score_x = self.score_x + 300
        self.back_x = self.high_score_x + 200
        self.current_shape_x = 320
        self.next_x = 620
        self.generation_x = 720
        self.agent_x = 620
        self.player_weights_x = 320

        # Define the initial vertical position for each row
        self.score_y = 20
        self.current_shape_y = self.score_y + self.vertical_spacing
        self.generation_y = self.current_shape_y + self.vertical_spacing
        self.agent_y = self.current_shape_y + self.vertical_spacing
        self.agent_y = self.current_shape_y + self.vertical_spacing
        self.player_weights_y = self.agent_y + self.vertical_spacing

        # Define the dimensions of the back button
        self.back_button_width = 100
        self.back_button_height = 50

        # Define the dimensions of the rectangles
        self.score_rect = pygame.Rect(self.score_x, self.score_y, 200, 40)
        self.high_score_rect = pygame.Rect(self.high_score_x, self.score_y, 200, 40)
        self.back_rect = pygame.Rect(self.back_x, self.score_y, self.back_button_width, self.back_button_height)
        self.current_shape_rect = pygame.Rect(self.current_shape_x, self.current_shape_y, 200, 40)
        self.next_shape_rect = pygame.Rect(self.next_x, self.current_shape_y, 200, 40)
        self.generation_rect = pygame.Rect(self.generation_x, self.generation_y, 200, 40)
        self.agent_rect = pygame.Rect(self.agent_x, self.agent_y, 200, 40)
        self.player_weights_rect = pygame.Rect(self.player_weights_x, self.player_weights_y, 300, 40)

    def render(self, game, current_player, highest_score, agent_type):
        """Render the game screen."""
        self.screen.fill(Colors.BACKGROUND_COLOR)

        self.render_score(game)
        self.render_high_score(highest_score)
        self.render_back_button()
        self.render_current_shape()
        self.render_next_shape()
        self.render_generation_number(current_player.generation_number)
        self.render_agent_type(agent_type)
        self.render_player_weights(current_player)
        self.player_weights_surface = self.title_font.render("Player " + str(current_player.number), True, Colors.white)

        if game.game_over:
            self.screen.blit(self.game_over_surface, (320, 450))

        game.draw(self.screen)
        pygame.display.update()

    def render_score(self, game):
        """Render the score."""
        self.screen.blit(self.score_surface, (self.score_x, self.score_y))
        score_value_surface = self.score_font.render(str(game.score), True, Colors.white)
        self.screen.blit(score_value_surface, (self.score_x, self.score_y + 35))

    def render_high_score(self, highest_score):
        """Render the high score."""
        self.screen.blit(self.high_score_surface, (self.high_score_x, self.score_y))
        high_score_value_surface = self.score_font.render(str(highest_score), True, Colors.white)
        self.screen.blit(high_score_value_surface, (self.high_score_x, self.score_y + 35))

    def render_back_button(self):
        """Render the back button."""
        back_color = Colors.light_blue
        pygame.draw.rect(self.screen, back_color, self.back_rect, border_radius=10)
        pygame.draw.rect(self.screen, Colors.dark_blue, self.back_rect, width=4, border_radius=10)
        self.screen.blit(self.back_surface, self.back_surface.get_rect(center=self.back_rect.center))

    def render_current_shape(self):
        """Render the current shape."""
        self.screen.blit(self.current_shape_surface, (self.current_shape_x + 6, self.current_shape_y))

    def render_next_shape(self):
        """Render the next shape."""
        self.screen.blit(self.next_shape_surface, (self.next_x, self.current_shape_y))

    def render_generation_number(self, generation_number):
        """Render the generation number."""
        self.screen.blit(self.generation_surface, (self.generation_x, self.generation_y))
        generation_value_surface = self.score_font.render(str(generation_number), True, Colors.white)
        self.screen.blit(generation_value_surface, (self.generation_x, self.generation_y + 35))

    def render_agent_type(self, agent_type):
        """Render the agent type."""
        self.screen.blit(self.agent_surface, (self.agent_x, self.agent_y))
        agent_type_surface = self.score_font.render(agent_type, True, Colors.white)
        self.screen.blit(agent_type_surface, (self.agent_x, self.agent_y + 35))

    def render_player_weights(self, current_player):
        """Render the player weights."""
        self.screen.blit(self.player_weights_surface, (self.player_weights_x, self.player_weights_y))
        player_details_text = f"Height: {current_player.height_weight:.2f}, " \
                              f"Lines Cleared: {current_player.lines_cleared_weight:.2f}, " \
                              f"Holes: {current_player.holes_weight:.2f}, " \
                              f"Blockades: {current_player.blockades_weight:.2f}"
        player_details_surface = self.score_font.render(player_details_text, True, Colors.white)
        self.screen.blit(player_details_surface, (self.player_weights_x, self.player_weights_y + 35))
