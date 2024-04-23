import random


class Agent:
    def __init__(self):
        self.agent_type = "AI"

    def make_move(self):
        return random.choice(["LEFT", "RIGHT", "DOWN", "ROTATE"])
