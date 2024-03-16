import pygame
import sys
import subprocess
from emulator import run_game



# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
DARK_BLUE = (3, 43, 73)
LIGHT_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)

# Set up the screen
screen = pygame.display.set_mode((1300, 700))
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# Load images
background_image = pygame.image.load("assets/backgrounds/background (X).jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
logo_image = pygame.image.load("logo.png").convert_alpha()

# Fonts
title_font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 20)

# Text surfaces
title_surface = title_font.render("Fast Tetris", True, WHITE)
play_surface = button_font.render("Play Yourself", True, WHITE)
ai_surface = button_font.render("Let AI do the work", True, WHITE)

# Button rects
button_width = 300
button_height = 60
play_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 - button_height, button_width, button_height)
ai_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 + 20, button_width, button_height)

# Game loop
while True:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw the logo
    logo_rect = logo_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(logo_image, logo_rect)

    # Draw the title
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
    screen.blit(title_surface, title_rect)

    # Draw the buttons
    play_color = LIGHT_BLUE
    ai_color = LIGHT_BLUE
    if play_rect.collidepoint(mouse_pos):
        if click:
            run_game()
        play_color = GRAY
    if ai_rect.collidepoint(mouse_pos):
        if click:
            # Placeholder for AI functionality (not implemented in this example)
            print("Let AI do the work...")
        ai_color = GRAY

    pygame.draw.rect(screen, play_color, play_rect)
    pygame.draw.rect(screen, ai_color, ai_rect)
    pygame.draw.rect(screen, DARK_BLUE, play_rect, 4)
    pygame.draw.rect(screen, DARK_BLUE, ai_rect, 4)

    # Align text to center of buttons
    play_text_rect = play_surface.get_rect(center=play_rect.center)
    ai_text_rect = ai_surface.get_rect(center=ai_rect.center)
    screen.blit(play_surface, play_text_rect)
    screen.blit(ai_surface, ai_text_rect)

    pygame.display.flip()
