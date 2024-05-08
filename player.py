from pathSearcher import PathSearcher
import time


class Player:
    def __init__(self, height_weight, lines_cleared_weight, holes_weight, blockades_weight):
        """
        Initializes a Player object with given weights for evaluating paths.

        Args:
            height_weight (float): Weight for height of the grid.
            lines_cleared_weight (float): Weight for number of lines cleared.
            holes_weight (float): Weight for number of holes in the grid.
            blockades_weight (float): Weight for number of blockades in the grid.
        """
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

    def get_path(self, game, current_grid):
        """
        Calculates the optimal path for the current game state and grid.

        Args:
            game: The Tetris game object.
            current_grid: The current grid state.

        Returns:
            list: The optimal path determined by the AI player.
        """
        self.game = game
        searcher = PathSearcher()
        self.All_Possible_Paths = searcher.calculate_paths(game, current_grid, self.height_weight,
                                                           self.lines_cleared_weight,
                                                           self.holes_weight, self.blockades_weight)

        print("Number OF Moves")
        print(str(self.All_Possible_Paths.__len__()))

        # game.grid.print_grid()
        optimal_path = self.choose_optimal_path()
        # optimal_path.print_details()

        # # Generate a single optimal path for testing
        # optimal_path = ["LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "ROTATE", "ROTATE", "ROTATE", "RIGHT",
        #                 "DOWN", "LEFT", "RIGHT",
        #                 "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "LEFT", "RIGHT", "DOWN"]

        return optimal_path

    def choose_optimal_path(self):
        """
        Chooses the optimal path among all possible paths based on their ranks.

        Returns:
            list: The optimal path determined by the AI player.
        """
        if not self.All_Possible_Paths:
            return None

        print("All paths ------------------------------------------")
        for path in self.All_Possible_Paths:
            path.print_details()

        # Find the path with the maximum rank using the max function
        optimal_path = max(self.All_Possible_Paths, key=lambda path: path.rank)
        print("optimal Path iss-----------------")
        optimal_path.print_details()

        # time.sleep(10)
        return optimal_path
