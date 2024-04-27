from pathSearcher import PathSearcher


class Player:
    def __init__(self, height_weight, lines_cleared_weight, holes_weight, blockades_weight):
        self.height_weight = height_weight
        self.lines_cleared_weight = lines_cleared_weight
        self.holes_weight = holes_weight
        self.blockades_weight = blockades_weight
        self.score = 0
        self.isAlive = True
        self.agent_type = "AI"
        self.All_Possible_Paths = []
        self.grid = None
        self.game = None

    def calculate_move_rank(self, height, lines_cleared, holes, blockades):
        move_rank = (
                self.height_weight * height +
                self.lines_cleared_weight * lines_cleared +
                self.holes_weight * holes +
                self.blockades_weight * blockades
        )
        return move_rank

    def get_path(self, game):
        # Set the grid, current_block, and next_block in self
        self.game = game
        searcher = PathSearcher()
        self.All_Possible_Paths = searcher.calculate_paths(game)

        # Generate a single optimal path for testing
        optimal_path = ["LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "ROTATE", "ROTATE", "ROTATE", "RIGHT",
                        "DOWN", "LEFT", "RIGHT",
                        "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "LEFT", "RIGHT", "DOWN"]

        return optimal_path

    def calculate_all_possible_paths(self, current_shape, grid):
        # Implement to calculate all possible paths for the current shape
        pass

    def choose_optimal_path(self):
        # Implement to choose the most optimal path from All_Possible_Paths
        pass
