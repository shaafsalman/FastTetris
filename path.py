class Path:
    """
    A class representing a path of moves for Tetris block movement.

    Attributes:
        moves (list): A list of moves representing block rotation and placement.
        height (int): The maximum height of the grid after block placement.
        lines_cleared (int): The number of lines cleared in the grid after block placement.
        holes (int): The number of holes in the grid after block placement.
        blockades (int): The number of blockades in the grid after block placement.
        game_over_move (bool): Indicates if the move results in a game over.
        rank (float): The rank assigned to the path based on different factors.
    """

    def __init__(self):
        """
        Initializes the Path class with default values.
        """
        self.moves = []
        self.height = 0
        self.lines_cleared = 0
        self.holes = 0
        self.blockades = 0
        self.game_over_move = False
        self.rank = 0

    def set_moves(self, moves):
        """
        Sets the list of moves for the path.

        Args:
            moves (list): A list of moves representing block rotation and placement.
        """
        self.moves = moves

    def set_attributes(self, height, lines_cleared, holes, blockades):
        """
        Sets the attributes of the path.

        Args:
            height (int): The maximum height of the grid after block placement.
            lines_cleared (int): The number of lines cleared in the grid after block placement.
            holes (int): The number of holes in the grid after block placement.
            blockades (int): The number of blockades in the grid after block placement.
        """
        self.height = height
        self.lines_cleared = lines_cleared
        self.holes = holes
        self.blockades = blockades

    def set_rank(self, rank):
        """
        Sets the rank of the path.

        Args:
            rank (float): The rank assigned to the path based on different factors.
        """
        self.rank = rank

    def set_game_over_move(self, game_over_move):
        """
        Sets whether the move results in a game over.

        Args:
            game_over_move (bool): Indicates if the move results in a game over.
        """
        self.game_over_move = game_over_move

    def set_path(self, moves, height, lines_cleared, holes, blockades, game_over_move):
        """
        Sets all attributes of the path.

        Args:
            moves (list): A list of moves representing block rotation and placement.
            height (int): The maximum height of the grid after block placement.
            lines_cleared (int): The number of lines cleared in the grid after block placement.
            holes (int): The number of holes in the grid after block placement.
            blockades (int): The number of blockades in the grid after block placement.
            game_over_move (bool): Indicates if the move results in a game over.
        """
        self.moves = moves
        self.height = height
        self.lines_cleared = lines_cleared
        self.holes = holes
        self.blockades = blockades
        self.game_over_move = game_over_move

    def print_details(self):
        """
        Prints the details of the path.
        """
        print("Moves:", self.moves)
        print("Height:", self.height)
        print("Lines Cleared:", self.lines_cleared)
        print("Holes:", self.holes)
        print("Blockades:", self.blockades)
        print("Rank:", self.rank)
        print("Game Over Move:", self.game_over_move)
