from pathSearcher import PathSearcher


class Player:
    def __init__(self, height_weight, lines_cleared_weight, holes_weight, blockades_weight):
        self.height_weight = height_weight
        self.lines_cleared_weight = lines_cleared_weight
        self.holes_weight = holes_weight
        self.blockades_weight = blockades_weight
        self.number = 0
        self.generation_number = 0
        self.score = 0
        self.isAlive = True
        self.agent_type = "AI"
        self.All_Possible_Paths = []
        self.grid = None
        self.game = None

    def get_path(self, game):
        # Set the grid, current_block, and next_block in self
        self.game = game
        searcher = PathSearcher()
        self.All_Possible_Paths = searcher.calculate_paths(game, self.height_weight, self.lines_cleared_weight,
                                                           self.holes_weight, self.blockades_weight)

        optimal_path = self.choose_optimal_path()
        optimal_path.print_details()

        # # Generate a single optimal path for testing
        # optimal_path = ["LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "ROTATE", "ROTATE", "ROTATE", "RIGHT",
        #                 "DOWN", "LEFT", "RIGHT",
        #                 "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "LEFT", "RIGHT", "DOWN"]

        return optimal_path

    def choose_optimal_path(self):
        if not self.All_Possible_Paths:
            return None  # Return None if there are no paths calculated

        # Find the path with the maximum rank using the max function
        optimal_path = max(self.All_Possible_Paths, key=lambda path: path.rank)
        return optimal_path
