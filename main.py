import pygame
import sys
import subprocess

import emulator
from emulator import TetrisGame
from ai_emulator import AITetrisGame
from colors import Colors

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
background_image = pygame.image.load("assets/backgrounds/background (X).jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonts
title_font = pygame.font.Font("assets/fonts/Poppins-Bold.ttf", 120)
button_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 28)

# Text surfaces
title_surface = title_font.render("Fast Tetris", True, Colors.white)
play_surface = button_font.render("Play Yourself", True, Colors.white)
ai_surface = button_font.render("Let AI do the work", True, Colors.white)

# Button rects
button_width, button_height = 300, 60
play_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 - 100, button_width, button_height)
ai_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 + 40, button_width, button_height)

# Feedback variables
play_clicked = False
ai_clicked = False

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

    # Draw buttons with feedback
    play_color = Colors.light_blue if not play_rect.collidepoint(mouse_pos) else Colors.green
    ai_color = Colors.light_blue if not ai_rect.collidepoint(mouse_pos) else Colors.green

    if play_rect.collidepoint(mouse_pos) and click:
        play_clicked = True
    elif ai_rect.collidepoint(mouse_pos) and click:
        ai_clicked = True

    # Draw buttons with feedback
    pygame.draw.rect(screen, play_color if not play_clicked else Colors.dark_blue, play_rect, border_radius=30)
    pygame.draw.rect(screen, ai_color if not ai_clicked else Colors.dark_blue, ai_rect, border_radius=30)

    # Align text to center of buttons
    screen.blit(play_surface, play_surface.get_rect(center=play_rect.center))
    screen.blit(ai_surface, ai_surface.get_rect(center=ai_rect.center))

    # Check for button click and start the corresponding game mode
    if play_clicked:
        tetris_game = TetrisGame()
        tetris_game.run_game()
        play_clicked = False  # Reset click status after starting the game
    elif ai_clicked:
        tetris_game = AITetrisGame()
        tetris_game.run_game()
        ai_clicked = False  # Reset click status after starting the game

    pygame.display.flip()