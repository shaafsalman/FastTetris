import random


class Agent:
    def __init__(self):
        pass

    def make_move(self):
        return random.choice(["LEFT", "RIGHT", "DOWN", "ROTATE"])
