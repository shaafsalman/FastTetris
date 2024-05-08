import os
import pygame
import sys
from random import uniform, sample
from game import Game
from graphic_renderer import Renderer
from player import Player
from config import GAConfig
from FastTetris.path import Path


def generate_crossover_players(num_players, top_players):
    """Generate players through crossover of top players."""
    crossover_players = []
    for _ in range(num_players):
        # Randomly select two parents for crossover
        parent1, parent2 = sample(top_players, 2)
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


class GA(Renderer):
    def __init__(self):
        super().__init__()

        # Genetic Algorithm parameters
        self.population_size = GAConfig.population_size
        self.mutation_rate = GAConfig.mutation_rate
        self.crossover_rate = GAConfig.crossover_rate
        self.population = []
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.current_generation = 1
        self.current_player_index = 0

        # Pygame event for game updates
        self.GAME_UPDATE = pygame.USEREVENT
        self.highest_score = self.game.highest_score
        pygame.time.set_timer(self.GAME_UPDATE, 60)

    def evolve_population(self):
        """Evolve the population using mutation and crossover."""
        self.population.sort(key=lambda x: x.score, reverse=True)
        top_players = self.population[:2]
        new_population = top_players + generate_random_players(5) + generate_crossover_players(5, top_players)
        self.population = new_population

    def initialize_population(self):
        """Initialize the population with random players."""
        for _ in range(self.population_size):
            height_weight = uniform(-5.0, 0.0)
            lines_cleared_weight = uniform(0.0, 15.0)
            holes_weight = uniform(-5.0, 0.0)
            blockades_weight = uniform(-5.0, 0.0)
            player = Player(height_weight, lines_cleared_weight, holes_weight, blockades_weight)
            self.population.append(player)

        self.initialize_population()
        for generation in range(self.current_generation, GAConfig.num_generations + 1):
            print(f"Generation {generation}")
            self.current_generation = generation
            self.play_generation()
            self.evolve_population()
            self.save_generation_details(generation)
            self.save_current_state()
            print(f"Best player's score in generation {generation}: {self.population[0].score}")
            self.clock.tick(2000)

    def play_game(self, current_player):
        """Play a game using the given player."""
        is_alive = True
        is_paused = False

        while is_alive:
            is_alive = self.handle_events(is_paused)

            if is_paused:
                continue

            current_grid = self.game.grid.copy()
            path = current_player.get_path(self.game, current_grid)
            moves = path.moves

            for move in moves:
                if self.game.game_over:
                    self.game.game_over = False
                    self.game.reset()
                    if self.game.score > self.highest_score:
                        self.highest_score = self.game.score

                self.execute_move(move)
                self.render(self.game, current_player, self.highest_score, "AI")
                pygame.time.delay(int(1000 / 50))

                if path.game_over_move or self.game.game_over:
                    is_alive = False
                    current_player.score = self.game.score
                    break

    def handle_events(self, is_paused):
        """Handle events during the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_rect.collidepoint(mouse_pos):
                    return True
        return False

    def execute_move(self, move):
        """Execute the given move."""
        if move == "LEFT":
            self.game.move_left()
        elif move == "RIGHT":
            self.game.move_right()
        elif move == "DOWN":
            self.game.move_down()
            self.game.update_score(0, 1)
        elif move == "ROTATE":
            self.game.rotate()

    def play_generation(self):
        """Play games for all players in the current generation."""
        for player_index in range(self.current_player_index, self.population_size):
            self.current_player_index = player_index
            player = self.population[player_index]
            player.generation_number = self.current_generation
            player.number = player_index + 1
            self.play_game(player)

    def save_generation_details(self, generation_number):
        """Save the details of each player in a record file for the generation."""
        folder_name = f"Generation_{generation_number}"
        folder_path = os.path.join("Generations", folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for player in self.population:
            file_name = f"Player_{player.number}.txt"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "w") as file:
                file.write(f"Player Number: {player.number}\n")
                file.write(f"Generation Number: {player.generation_number}\n")
                file.write(f"Height Weight: {player.height_weight}\n")
                file.write(f"Lines Cleared Weight: {player.lines_cleared_weight}\n")
                file.write(f"Holes Weight: {player.holes_weight}\n")
                file.write(f"Blockades Weight: {player.blockades_weight}\n")
                file.write(f"Score: {player.score}\n")

    def save_current_state(self):
        """Save the current state (generation number and current player index)."""
        with open("current_state.txt", "w") as file:
            file.write(f"{self.current_generation}\n")
            file.write(f"{self.current_player_index}\n")

    def run(self):
        """Run the genetic algorithm."""
        if os.path.exists("current_state.txt"):
            with open("current_state.txt", "r") as file:
                state = file.readlines()
                self.current_generation = int(state[0].strip())
                self.current_player_index = int(state[1].strip())


if __name__ == "__main__":
    ga = GA()
    turn_off_music()
    ga.run()
