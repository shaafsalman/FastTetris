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
            #
            # self.height_weight * path.height +
            # self.lines_cleared_weight * path.lines_cleared +
            # self.holes_weight * path.holes
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

        for rotation in range(4):
            for col in range(game.grid.num_cols):
                print ("the col is---------------------")
                print(col)
                current_grid = grid.copy()
                game_copy = game.copy()
                block = game.current_block.copy()
                moves = self.calculate_block_moves(current_grid, col, rotation)
                holes, blockades, full_rows, max_height = game_copy.apply_moves_to_grid(moves)
                path = self.create_path(moves, holes, blockades, full_rows, max_height)
                self.paths.append(path)

        return self.paths

    def calculate_block_moves(self, grid, col, rotation):
        moves = []
        moves.extend(["ROTATE"] * rotation)
        moves.extend(["RIGHT"] * col)
        moves.extend(["DOWN"] * grid.num_rows)

        return moves

    def create_path(self, moves, holes, blockades, full_rows, max_height):
        path = Path()
        path.set_moves(moves)

        height_of_path = max_height
        lines_cleared_of_path = full_rows
        holes_of_path = holes
        blockades_of_path = blockades

        path.set_attributes(height_of_path, lines_cleared_of_path, holes_of_path, blockades_of_path)

        rank = self.calculate_move_rank(path)
        path.set_rank(rank)
        # path.set_game_over_move(grid.is_grid_full())

        return path
