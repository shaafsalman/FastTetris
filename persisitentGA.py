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
    """Generate players through crossover of top players."""
    crossover_players = []
    for _ in range(num_players):
        # Randomly select two parents for crossover
        parent1, parent2 = random.sample(top_players, 2)
        # Perform crossover
        height_weight = uniform(parent1.height_weight, parent2.height_weight)
        lines_cleared_weight = uniform(parent1.lines_cleared_weight, parent2.lines_cleared_weight)
        holes_weight = uniform(parent1.holes_weight, parent2.holes_weight)
        blockades_weight = uniform(parent1.blockades_weight, parent2.blockades_weight)
        player = Player(height_weight, lines_cleared_weight, holes_weight, blockades_weight)
        crossover_players.append(player)
    return crossover_players


def generate_random_players(num_players):
    """Generate random players with random weights."""
    random_players = []
    for _ in range(num_players):
        height_weight = uniform(-1.0, 1.0)
        lines_cleared_weight = uniform(-1.0, 1.0)
        holes_weight = uniform(-1.0, 1.0)
        blockades_weight = uniform(-1.0, 1.0)
        player = Player(height_weight, lines_cleared_weight, holes_weight, blockades_weight)
        random_players.append(player)
    return random_players


class persistent_ga(Renderer):
    def __init__(self):
        super().__init__()
        self.population_size = GAConfig.population_size
        self.mutation_rate = GAConfig.mutation_rate
        self.population = []
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.generation_count = 0  # Track the number of generations processed

        self.load_generation_data()  # Load previous generation data
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

            # height_weight = -15
            # lines_cleared_weight = 5
            # holes_weight = -5
            # blockades_weight = -1

            # Create player object with random weights
            player = Player(height_weight, lines_cleared_weight, holes_weight, blockades_weight)
            self.population.append(player)

    def run(self):
        # Check if previous generation data exists
        if os.path.exists("generation_data.txt"):
            self.load_generation_data()  # Load previous generation data
        else:
            self.initialize_population()  # Initialize population if no previous data found

        for generation in range(self.generation_count + 1, GAConfig.num_generations + 1):
            print(f"Generation {generation}")
            self.play_generation(generation)
            self.evolve_population()
            self.save_generation_data(generation)  # Save generation data

            print(f"Best player's score in generation {generation}: {self.population[0].score}")
            self.clock.tick(2000)

            print(f"Generation count: {self.generation_count}")

            print("All generations completed.")

        # # Check if it's time to mutate
        # if self.generation_count % 5 == 0:
        #     self.mutate_population()

    def save_generation_data(self, generation_number):
        with open("generation_data.txt", "w") as file:
            file.write(f"Generation: {generation_number}\n")
            for i, player in enumerate(self.population):
                file.write(
                    f"Player {i + 1} Weights: {player.height_weight}, {player.lines_cleared_weight}, {player.holes_weight}, {player.blockades_weight}\n")

    def load_generation_data(self):
        if os.path.exists("generation_data.txt"):
            with open("generation_data.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("Generation:"):
                        self.generation_count = int(line.split(":")[1])
                    elif line.startswith("Player"):
                        weights = [float(val) for val in line.split(":")[1].strip().split(',')]
                        player = Player(*weights)
                        self.population.append(player)

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
        """Evolve the population using mutation and crossover."""
        # Sort the population based on scores
        self.population.sort(key=lambda x: x.score, reverse=True)
        # Take the top two players with the highest score
        top_players = self.population[:2]
        # Generate new population with mutation and crossover
        new_population = top_players + generate_random_players(5) + generate_crossover_players(5,
                                                                                               top_players)
        # Replace the old population with the new one
        self.population = new_population


if __name__ == "__main__":
    ga = persistent_ga()
    ga.run()
