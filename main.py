import pygame
import sys
from config import GAConfig
from emulator import Human_Emulator
from GA import GA
from FastTetris.colors import Colors


def initialize_pygame():
    """Initialize Pygame"""
    pygame.init()


def setup_screen():
    """Set up the screen"""
    return pygame.display.set_mode((GAConfig.SCREEN_WIDTH, GAConfig.SCREEN_HEIGHT))


def load_images():
    """Load images"""
    background_image = pygame.image.load(GAConfig.BACKGROUND_IMAGE_PATH).convert()
    return pygame.transform.scale(background_image, (GAConfig.SCREEN_WIDTH, GAConfig.SCREEN_HEIGHT))


def load_fonts():
    """Load fonts"""
    title_font = pygame.font.Font(GAConfig.TITLE_FONT_PATH, GAConfig.TITLE_FONT_SIZE)
    button_font = pygame.font.Font(GAConfig.BUTTON_FONT_PATH, GAConfig.BUTTON_FONT_SIZE)
    return title_font, button_font


def create_text_surfaces(title_font, button_font):
    """Create text surfaces"""
    title_surface = title_font.render("Fast Tetris", True, Colors.white)
    play_surface = button_font.render("Play Yourself", True, Colors.white)
    ai_surface = button_font.render("Let AI do the work", True, Colors.white)
    return title_surface, play_surface, ai_surface


def create_button_rects():
    """Create button rects"""
    play_rect = pygame.Rect((GAConfig.SCREEN_WIDTH - GAConfig.BUTTON_WIDTH) // 2,
                            GAConfig.SCREEN_HEIGHT // 2 - 100, GAConfig.BUTTON_WIDTH, GAConfig.BUTTON_HEIGHT)
    ai_rect = pygame.Rect((GAConfig.SCREEN_WIDTH - GAConfig.BUTTON_WIDTH) // 2,
                          GAConfig.SCREEN_HEIGHT // 2 + 40, GAConfig.BUTTON_WIDTH, GAConfig.BUTTON_HEIGHT)
    return play_rect, ai_rect


def handle_events(play_rect, ai_rect):
    """Handle events"""
    play_clicked = False
    ai_clicked = False
    mouse_pos = pygame.mouse.get_pos()
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True
    if play_rect.collidepoint(mouse_pos) and click:
        play_clicked = True
    elif ai_rect.collidepoint(mouse_pos) and click:
        ai_clicked = True
    return play_clicked, ai_clicked


def draw_buttons(screen, play_rect, ai_rect, play_surface, ai_surface, play_clicked, ai_clicked):
    """Draw buttons with feedback"""
    play_color = Colors.light_blue if not play_rect.collidepoint(pygame.mouse.get_pos()) else Colors.green
    ai_color = Colors.light_blue if not ai_rect.collidepoint(pygame.mouse.get_pos()) else Colors.green
    pygame.draw.rect(screen, play_color if not play_clicked else Colors.dark_blue, play_rect, border_radius=30)
    pygame.draw.rect(screen, ai_color if not ai_clicked else Colors.dark_blue, ai_rect, border_radius=30)
    screen.blit(play_surface, play_surface.get_rect(center=play_rect.center))
    screen.blit(ai_surface, ai_surface.get_rect(center=ai_rect.center))


def main():
    """Main function"""
    initialize_pygame()
    screen = setup_screen()
    background_image = load_images()
    title_font, button_font = load_fonts()
    title_surface, play_surface, ai_surface = create_text_surfaces(title_font, button_font)
    play_rect, ai_rect = create_button_rects()
    play_clicked = False
    ai_clicked = False

    # Main loop
    while True:
        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        screen.blit(title_surface,
                    title_surface.get_rect(center=(GAConfig.SCREEN_WIDTH // 2, GAConfig.SCREEN_HEIGHT // 8)))
        play_clicked, ai_clicked = handle_events(play_rect, ai_rect)
        draw_buttons(screen, play_rect, ai_rect, play_surface, ai_surface, play_clicked, ai_clicked)
        if play_clicked:
            tetris_game = Human_Emulator()
            tetris_game.run()
            play_clicked = False  # Reset click status after starting the game
        elif ai_clicked:
            tetris_game = GA()
            tetris_game.run()
            ai_clicked = False  # Reset click status after starting the game
        pygame.display.flip()


if __name__ == "__main__":
    main()
