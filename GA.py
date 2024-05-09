import os
import pygame
import sys
from random import random, uniform
from game import Game
from colors import Colors
from graphic_renderer import Renderer
from player import Player
from config import GAConfig
import random
from path import Path


def generate_crossover_players(num_players, top_players):
    crossover_players = []
    for _ in range(num_players):
        parent1, parent2 = random.sample(top_players, 2)
        crossover_point = random.randint(1, len(parent1) - 1)
        height_weight = parent1[:crossover_point] + parent2[crossover_point:]
        lines_cleared_weight = parent2[:crossover_point] + parent1[crossover_point:]
        holes_weight = parent1[crossover_point:] + parent2[:crossover_point]
        blockades_weight = parent2[crossover_point:] + parent1[:crossover_point]
        player = Player(height_weight, lines_cleared_weight, holes_weight, blockades_weight)
        crossover_players.append(player)
    return crossover_players



def generate_random_players(num_players):
    """Generate random players with random weights."""
    random_players = []
    for _ in range(num_players):
        height_weight = uniform(-15.0, 0.0)
        lines_cleared_weight = uniform(0.0, 15.0)
        holes_weight = uniform(-15.0, 0.0)
        blockades_weight = uniform(-15.0, 0.0)
        player = Player(height_weight, lines_cleared_weight, holes_weight, blockades_weight)
        random_players.append(player)
    return random_players


class GA(Renderer):
    def __init__(self):
        super().__init__()
        self.population_size = GAConfig.population_size
        self.mutation_rate = GAConfig.mutation_rate
        self.population = []
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.generation_count = 0  # Track the number of generations processed

        self.GAME_UPDATE = pygame.USEREVENT
        self.highest_score = self.game.highest_score
        pygame.time.set_timer(self.GAME_UPDATE, 60)

    def initialize_population(self):
        # Initialize the population with random players
        for _ in range(self.population_size):
            # Generate random weights for player attributes
            height_weight = uniform(-15.0, 0.0)
            lines_cleared_weight = uniform(0.0, 15.0)
            holes_weight = uniform(-15.0, 0.0)
            blockades_weight = uniform(-15.0, 0.0)

            player = Player(height_weight, lines_cleared_weight, holes_weight, blockades_weight)
            self.population.append(player)

    def run(self):
        self.initialize_population()
        for generation in range(GAConfig.num_generations):
            print(f"Generation {generation + 1}")
            self.play_generation(generation + 1)
            self.evolve_population()

            print(f"Best player's score in generation {generation + 1}: {self.population[0].score}")
            self.clock.tick(2000)

            # Increment generation count
            self.generation_count += 1
            print(f"Generation count: {self.generation_count}")  # Add this line

            # Check if it's time to mutate
            if self.generation_count % 5 == 0:
                self.mutate_population()


    def mutate_population(self):
        mutation_count = int(len(self.population) * self.mutation_rate)
        for _ in range(mutation_count):
            index = random.randint(0, len(self.population) - 1)
            player = self.population[index]

            player.height_weight += random.uniform(-15.0, 0.0)
            player.lines_cleared_weight += random.uniform(0, 15.0)
            player.holes_weight += random.uniform(-15.0, 0.0)
            player.blockades_weight += random.uniform(-15.0, 0.0)

    def play_game(self, current_player):
        # Initialize variables
        is_alive = True
        is_paused = False

        # Main game loop
        while is_alive:
            # Check for events and handle pause
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_paused = not is_paused  # Toggle pause state on space press
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.back_rect.collidepoint(mouse_pos):
                        return

            # Pause game if needed
            if is_paused:
                continue

            # Get the current grid state
            current_grid = self.game.grid.copy()

            # Get the path from the current player
            path = Path()

            # Get the path from the current player
            path = current_player.get_path(self.game, current_grid)
            moves = path.moves

            # Execute each move in the path
            for move in moves:
                # Check for game over
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
                self.render(self.game, current_player, self.highest_score, "AI", self.game.lines_cleared)

                # Delay for smooth rendering
                pygame.time.delay(int(GAConfig.game_speed / 50))

                # Check for game over
                if path.game_over_move or self.game.game_over:
                    is_alive = False
                    current_player.score = self.game.score
                    break

    def handle_events(self, is_paused):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_rect.collidepoint(mouse_pos):
                    return True  # Exit the game loop

        return False

    def play_generation(self, generation_number):
        """Play games for all players in the current generation."""
        player_number = 1
        for player in self.population:
            player.generation_number = generation_number
            player.number = player_number
            self.play_game(player)
            player_number += 1
            self.game.lines_cleared = 0

    def evolve_population(self):
        """Evolve the population using crossover."""
        self.population.sort(key=lambda x: x.score, reverse=True)
        top_players = self.population[:2]
        new_population = top_players + generate_random_players(5) + generate_crossover_players(5, top_players)
        self.population = new_population


if __name__ == "__main__":
    ga = GA()
    ga.run()
