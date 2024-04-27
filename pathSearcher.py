from path import Path


class PathSearcher:
    def __init__(self):
        self.paths = []
        self.game = None

    def calculate_paths(self, game):
        self.game = game
        current_grid = game.grid.grid

        for col in range(game.grid.num_cols):
            for rotation in range(4):
                block = game.current_block.copy()  # Create a copy of the current block
                block.rotate()  # Rotate the block to the current rotation
                if col + block.width <= game.grid.num_cols:  # Check if block can fit in the current column
                    row = 0
                    moves = []  # List to record the moves
                    while game.grid.can_place_block(block, row, col):  # Move the block down until it can't go further
                        moves.append("DOWN")  # Record the move
                        row += 1
                    if row > 0:  # If the block can be placed at least once
                        for _ in range(col):
                            moves.append("LEFT")  # Record the move to move the block left
                        moves.append("ROTATE" * rotation)  # Record the rotation moves
                        # Record the move to move the block up (to its original position)
                        for _ in range(game.grid.num_rows - row):
                            moves.append("UP")
                        for _ in range(col, game.grid.num_cols - block.width):
                            moves.append("RIGHT")  # Record the move to move the block right
                        path = Path()
                        path.set_moves(moves)  # Set the recorded moves as the move sequence
                        path.set_weights(0.5, 0.3, 0.2, 0.1)  # Example weights
                        path.set_game_over_move(False)  # Example game over move
                        print(f"Path generated: {moves}")  # Print the generated path
                        self.paths.append(path)

        return self.paths
