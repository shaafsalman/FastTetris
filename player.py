import random


class Player:
    def __init__(self, height_weight, lines_cleared_weight, holes_weight, blockades_weight):
        self.height_weight = height_weight
        self.lines_cleared_weight = lines_cleared_weight
        self.holes_weight = holes_weight
        self.blockades_weight = blockades_weight
        self.score = 0
        self.alive = True

    def calculate_move_rank(self, height, lines_cleared, holes, blockades):
        move_rank = (self.height_weight * height +
                     self.lines_cleared_weight * lines_cleared +
                     self.holes_weight * holes +
                     self.blockades_weight * blockades)
        return move_rank

    def play_game(self):
        self.score, self.alive = self.simulate_game()

    def simulate_game(self):
        score = random.randint(0, 1000)
        alive = True
        return score, alive

    def get_score(self):
        return self.score

    def is_alive(self):
        return self.alive
