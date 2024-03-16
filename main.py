import pygame
import sys

import emulator
from emulator import TetrisGame
from colors import  Colors

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1300, 700

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
background_image = pygame.image.load("assets/backgrounds/background (X).jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonts
title_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 120)
button_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 28)

# Text surfaces
title_surface = title_font.render("Fast Tetris", True, Colors.WHITE)
play_surface = button_font.render("Play Yourself", True, Colors.WHITE)
ai_surface = button_font.render("Let AI do the work", True, Colors.WHITE)

# Button rects
button_width, button_height = 300, 60
play_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 - 100, button_width, button_height)
ai_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 + 40, button_width, button_height)

# Main loop
while True:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True

    # Draw background, logo, and title
    screen.blit(background_image, (0, 0))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
    screen.blit(title_surface, title_rect)

    # Draw buttons
    play_color = Colors.LIGHT_BLUE if not play_rect.collidepoint(mouse_pos) else Colors.GRAY
    ai_color = Colors.LIGHT_BLUE if not ai_rect.collidepoint(mouse_pos) else Colors.GRAY
    if play_rect.collidepoint(mouse_pos) and click:
        tetris_game = TetrisGame()
        tetris_game.run_game()
    pygame.draw.rect(screen, play_color, play_rect, border_radius=30)
    pygame.draw.rect(screen, ai_color, ai_rect, border_radius=30)
    pygame.draw.rect(screen, Colors.DARK_BLUE, play_rect, width=4, border_radius=30)
    pygame.draw.rect(screen, Colors.DARK_BLUE, ai_rect, width=4, border_radius=30)

    # Align text to center of buttons
    screen.blit(play_surface, play_surface.get_rect(center=play_rect.center))
    screen.blit(ai_surface, ai_surface.get_rect(center=ai_rect.center))

    pygame.display.flip()
