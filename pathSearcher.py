from path import Path


class PathSearcher:
    def __init__(self):
        self.paths = []
        self.game = None
        self.height_weight = 0
        self.lines_cleared_weight = 0
        self.holes_weight = 0
        self.blockades_weight = 0

    def calculate_move_rank(self, path):
        move_rank = (
                self.height_weight * path.height +
                self.lines_cleared_weight * path.lines_cleared +
                self.holes_weight * path.holes +
                self.blockades_weight * path.blockades
        )
        return move_rank

    def set_weights(self, height_weight, lines_cleared_weight, holes_weight, blockades_weight):
        self.height_weight = height_weight
        self.lines_cleared_weight = lines_cleared_weight
        self.holes_weight = holes_weight
        self.blockades_weight = blockades_weight
        print("PLayer Weights")
        print(self.height_weight, self.lines_cleared_weight, self.holes_weight, self.blockades_weight)

    def calculate_paths(self, game, grid, player_height_weight, player_lines_cleared_weight, player_holes_weight,
                        player_blockades_weight):
        self.set_weights(player_height_weight, player_lines_cleared_weight, player_holes_weight,
                         player_blockades_weight)

        for col in range(game.grid.num_cols):
            current_grid = grid.copy()
            block = game.current_block.copy()
            moves = self.calculate_block_moves(game, current_grid, block, col)
            path = self.create_path(moves, current_grid)
            self.paths.append(path)

        return self.paths

    def calculate_block_moves(self, game, grid, block, col):
        moves = []
        rotations = block.number_of_rotations
        for rotation in range(rotations):
            block.rotate()
            if col + block.width <= game.grid.num_cols:
                row = 0
                while grid.can_place_block(block, row, col):
                    moves.append("DOWN")
                    row += 1

                if row > 0:
                    for _ in range(col):
                        moves.append("LEFT")
                    moves.append("ROTATE")
                    for _ in range(grid.num_rows - row):
                        moves.append("UP")
                    for _ in range(col, game.grid.num_cols - block.width):
                        moves.append("RIGHT")
        return moves

    def create_path(self, moves, grid):
        path = Path()
        path.set_moves(moves)

        height_of_path = grid.calculate_height()
        lines_cleared_of_path = 0
        holes_of_path = grid.calculate_holes()
        blockades_of_path = grid.calculate_blockades()

        path.set_attributes(height_of_path, lines_cleared_of_path, holes_of_path, blockades_of_path)

        rank = self.calculate_move_rank(path)
        path.set_rank(rank)
        path.set_game_over_move(grid.is_grid_full())

        return path



