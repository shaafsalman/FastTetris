from random import random
import pygame
import sys

from game import Game
from colors import Colors
from graphic_renderer import Renderer
from player import Player
from random import uniform


class GA(Renderer):
    def __init__(self, population_size, mutation_rate, crossover_rate):
        super().__init__()
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []
        self.clock = pygame.time.Clock()
        self.game = Game()

        self.GAME_UPDATE = pygame.USEREVENT
        self.highest_score = self.game.highest_score
        pygame.time.set_timer(self.GAME_UPDATE, 200)

    def initialize_population(self):
        # Initialize the population with random players
        for _ in range(self.population_size):
            # Generate random weights for player attributes
            height_weight = uniform(-1.0, 1.0)
            lines_cleared_weight = uniform(-1.0, 1.0)
            holes_weight = uniform(-1.0, 1.0)
            blockades_weight = uniform(-1.0, 1.0)

            # Create player object with random weights
            player = Player(height_weight, lines_cleared_weight, holes_weight, blockades_weight)
            self.population.append(player)

    def play_game(self, current_player):
        # Get the moves from the current player
        path = current_player.get_path(self.game)
        moves = path.moves
        is_alive = True

        # Iterate through each move
        while is_alive:

            for move in moves:
                # print(move)
                if self.game.game_over:
                    self.game.game_over = False
                    self.game.reset()
                    if self.game.score > self.highest_score:
                        self.highest_score = self.game.score

                # Execute the move
                if move == "LEFT":
                    self.game.move_left()
                elif move == "RIGHT":
                    self.game.move_right()
                elif move == "DOWN":
                    self.game.move_down()
                    self.game.update_score(0, 1)
                elif move == "ROTATE":
                    self.game.rotate()

                # Render the game state after each move
                self.render(self.game, current_player, self.highest_score, "AI")

                pygame.time.delay(int(1000 / 50))
                if path.game_over_move or self.game.game_over:
                    is_alive = False
                # Check for any events during the delay
                if self.handle_events():
                    break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_rect.collidepoint(mouse_pos):
                    return True

        return False  # No Back button click

    def run(self, num_generations):
        self.initialize_population()
        for generation in range(num_generations):
            if self.handle_events():
                break

            print(f"Generation {generation + 1}")
            player_number = 1
            for player in self.population:
                player.generation_number = generation + 1
                player.number = player_number
                self.play_game(player)
                player_number += 1
            # self.evolve()  # Uncomment this if needed
            print(f"Best player's score in generation {generation + 1}: {self.population[0].score}")
            self.clock.tick(2000)


if __name__ == "__main__":
    ga = GA(population_size=10, mutation_rate=0.1, crossover_rate=0.5)
    ga.game.turn_off_music()
    ga.run(num_generations=10)
