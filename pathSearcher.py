from FastTetris.path import Path


def calculate_block_moves(grid, col, rotation):
    """
    Calculates the moves for block rotation and placement based on column and rotation.

    Args:
        grid: The grid representing the current state of the game.
        col (int): The column index for block placement.
        rotation (int): The rotation index for block rotation.

    Returns:
        list: A list of moves representing block rotation and placement.
    """
    moves = []
    moves.extend(["ROTATE"] * rotation)
    moves.extend(["RIGHT"] * col)
    moves.extend(["DOWN"] * grid.num_rows)

    return moves


class PathSearcher:
    """
    A class responsible for searching and analyzing paths for Tetris block movement.

    Attributes:
        paths (list): A list to store the paths found during the search.
        game: The Tetris game instance.
        height_weight (float): Weight assigned to the height of the block.
        lines_cleared_weight (float): Weight assigned to the number of lines cleared.
        holes_weight (float): Weight assigned to the number of holes in the grid.
        blockades_weight (float): Weight assigned to the number of blockades in the grid.
    """

    def __init__(self):
        """
        Initializes the PathSearcher class.
        """
        self.paths = []
        self.game = None
        self.height_weight = 0
        self.lines_cleared_weight = 0
        self.holes_weight = 0
        self.blockades_weight = 0

    def calculate_move_rank(self, path):
        """
        Calculates the rank of a given path based on weights assigned to different factors.

        Args:
            path (Path): The path to calculate the rank for.

        Returns:
            float: The calculated rank for the path.
        """
        move_rank = (
                self.height_weight * path.height +
                self.lines_cleared_weight * path.lines_cleared +
                self.holes_weight * path.holes +
                self.blockades_weight * path.blockades


            # self.height_weight * path.height +
            # self.lines_cleared_weight * path.lines_cleared +
            # self.holes_weight * path.holes
        )
        return move_rank

    def set_weights(self, height_weight, lines_cleared_weight, holes_weight, blockades_weight):
        """
        Sets the weights for different factors used in calculating path ranks.

        Args:
            height_weight (float): Weight assigned to the height of the block.
            lines_cleared_weight (float): Weight assigned to the number of lines cleared.
            holes_weight (float): Weight assigned to the number of holes in the grid.
            blockades_weight (float): Weight assigned to the number of blockades in the grid.
        """
        self.height_weight = height_weight
        self.lines_cleared_weight = lines_cleared_weight
        self.holes_weight = holes_weight
        self.blockades_weight = blockades_weight
        print("Player Weights")
        print(self.height_weight, self.lines_cleared_weight, self.holes_weight, self.blockades_weight)

    def calculate_paths(self, game, grid, player_height_weight, player_lines_cleared_weight, player_holes_weight,
                        player_blockades_weight):
        """
        Calculates all possible paths for block movement based on the current game state and grid.

        Args:
            game: The Tetris game instance.
            grid: The grid representing the current state of the game.
            player_height_weight (float): Weight assigned to the height of the block.
            player_lines_cleared_weight (float): Weight assigned to the number of lines cleared.
            player_holes_weight (float): Weight assigned to the number of holes in the grid.
            player_blockades_weight (float): Weight assigned to the number of blockades in the grid.

        Returns:
            list: A list containing all the calculated paths.
        """
        self.set_weights(player_height_weight, player_lines_cleared_weight, player_holes_weight,
                         player_blockades_weight)

        for rotation in range(4):
            for col in range(game.grid.num_cols):
                print("The column is ---------------------")
                print(col)
                current_grid = grid.copy()
                game_copy = game.copy()
                block = game.current_block.copy()
                moves = calculate_block_moves(current_grid, col, rotation)
                holes, blockades, full_rows, max_height = game_copy.apply_moves_to_grid(moves)
                path = self.create_path(moves, holes, blockades, full_rows, max_height)
                self.paths.append(path)

        return self.paths

    def create_path(self, moves, holes, blockades, full_rows, max_height):
        """
        Creates a Path object based on the given parameters.

        Args:
            moves (list): A list of moves representing block rotation and placement.
            holes (int): The number of holes in the grid after block placement.
            blockades (int): The number of blockades in the grid after block placement.
            full_rows (int): The number of full rows in the grid after block placement.
            max_height (int): The maximum height of the grid after block placement.

        Returns:
            Path: The created Path object.
        """
        path = Path()
        path.set_moves(moves)

        height_of_path = max_height
        lines_cleared_of_path = full_rows
        holes_of_path = holes
        blockades_of_path = blockades

        path.set_attributes(height_of_path, lines_cleared_of_path, holes_of_path, blockades_of_path)

        rank = self.calculate_move_rank(path)
        path.set_rank(rank)

        return path
