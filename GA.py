from random import random
from player import Player


class GA:
    def __init__(self, population_size, mutation_rate, crossover_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []

    def initialize_population(self):
        # Initialize the population with random players
        for _ in range(self.population_size):
            player = Player()
            self.population.append(player)

    def selection(self):
        self.population.sort(key=lambda x: x.score, reverse=True)
        parents = self.population[:self.population_size // 2]
        return parents

    def crossover(self, parent1, parent2):
        offspring = Player()
        offspring.height_weight = parent1.height_weight if random.random() < 0.5 else parent2.height_weight
        offspring.lines_cleared_weight = parent1.lines_cleared_weight if random.random() < 0.5 else parent2.lines_cleared_weight
        offspring.holes_weight = parent1.holes_weight if random.random() < 0.5 else parent2.holes_weight
        offspring.blockades_weight = parent1.blockades_weight if random.random() < 0.5 else parent2.blockades_weight
        return offspring

    def mutation(self, player):
        # Mutate player's attributes based on mutation rate
        if random.random() < self.mutation_rate:
            player.height_weight += random.uniform(-0.1, 0.1)
        if random.random() < self.mutation_rate:
            player.lines_cleared_weight += random.uniform(-0.1, 0.1)
        if random.random() < self.mutation_rate:
            player.holes_weight += random.uniform(-0.1, 0.1)
        if random.random() < self.mutation_rate:
            player.blockades_weight += random.uniform(-0.1, 0.1)

    def evolve(self):
        # Select parents for crossover
        parents = self.selection()
        new_population = []
        # Perform crossover and mutation to generate new population
        while len(new_population) < self.population_size:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            offspring = self.crossover(parent1, parent2)
            self.mutation(offspring)
            new_population.append(offspring)
        # Update population with new generation
        self.population = new_population

    def run(self, num_generations):
        # Run the genetic algorithm for a specified number of generations
        self.initialize_population()
        for generation in range(num_generations):
            print(f"Generation {generation + 1}")
            for player in self.population:
                player.play_game()
            self.evolve()
            # Print the best player's score in each generation
            print(f"Best player's score in generation {generation + 1}: {self.population[0].score}")
