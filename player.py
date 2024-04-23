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

    def calculate_move_rank(self, height, lines_cleared, holes, blockades):
        move_rank = (
            self.height_weight * height +
            self.lines_cleared_weight * lines_cleared +
            self.holes_weight * holes +
            self.blockades_weight * blockades
        )
        return move_rank

    def getPath(self, grid, current_block, next_block):
        # Set the grid, current_block, and next_block in self
        self.grid = grid
        self.current_block = current_block
        self.next_block = next_block

        # Generate a single optimal path for testing
        optimal_path = ["LEFT", "RIGHT", "DOWN", "LEFT", "RIGHT", "DOWN"]
        return optimal_path

    def calculate_all_possible_paths(self, current_shape, grid):
        # Implement to calculate all possible paths for the current shape
        pass

    def choose_optimal_path(self):
        # Implement to choose the most optimal path from All_Possible_Paths
        pass


