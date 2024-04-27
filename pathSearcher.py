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

    def calculate_paths(self, game, player_height_weight, player_lines_cleared_weight, player_holes_weight,
                        player_blockades_weight):

        self.set_weights(player_height_weight, player_lines_cleared_weight, player_holes_weight,
                         player_blockades_weight)

        self.game = game
        current_grid = game.grid.copy()  # Create a copy of the current grid
        print("In calculate path")

        for col in range(game.grid.num_cols):
            # print("In column traverser")
            block = game.current_block.copy()  # Create a copy of the current block
            rotations = block.number_of_rotations  # Get the number of rotations for the current block
            # print("Block is " + block.name + " rotations " + str(rotations))

            old_height_of_path = current_grid.calculate_height()
            old_lines_cleared_of_path = 1
            old_holes_of_path = current_grid.calculate_holes()
            old_blockades_of_path = current_grid.calculate_blockades()
            print("old")
            print(old_height_of_path, old_lines_cleared_of_path, old_holes_of_path)

            for rotation in range(rotations):  # Iterate over the number of rotations
                block.rotate()  # Rotate the block to the current rotation
                if col + block.width <= game.grid.num_cols:  # Check if block can fit in the current column
                    row = 0
                    moves = []  # List to record the moves
                    while current_grid.can_place_block(block, row,
                                                       col):  # Move the block down until it can't go further
                        moves.append("DOWN")  # Record the move
                        row += 1
                    if row > 0:  # If the block can be placed at least once
                        for _ in range(col):
                            moves.append("LEFT")  # Record the move to move the block left
                        moves.extend(["ROTATE"])  # Record the rotation moves
                        # Record the move to move the block up (to its original position)
                        for _ in range(game.grid.num_rows - row):
                            moves.append("UP")
                        for _ in range(col, game.grid.num_cols - block.width):
                            moves.append("RIGHT")  # Record the move to move the block right
                        path = Path()
                        path.set_moves(moves)  # Set the recorded moves as the move sequence

                        # Example calculations for weights

                        new_height_of_path = current_grid.calculate_height()
                        new_lines_cleared_of_path = 1
                        new_holes_of_path = current_grid.calculate_holes()
                        new_blockades_of_path = current_grid.calculate_blockades()

                        print("new")
                        print(new_height_of_path, new_lines_cleared_of_path, new_holes_of_path)

                        height_of_path = old_height_of_path - new_height_of_path
                        lines_cleared_of_path = 0
                        holes_of_path = old_holes_of_path - new_holes_of_path
                        blockades_of_path = old_blockades_of_path - new_blockades_of_path

                        # Set the calculated values
                        path.set_attributes(height_of_path, lines_cleared_of_path, holes_of_path, blockades_of_path)

                        # Calculate move rank based on the current path
                        rank = self.calculate_move_rank(path)

                        # Set the rank to the path
                        path.set_rank(rank)
                        path.set_game_over_move(current_grid.is_grid_full())
                        # print(f"Path generated: {moves}")  # Print the generated path
                        self.paths.append(path)

        return self.paths
