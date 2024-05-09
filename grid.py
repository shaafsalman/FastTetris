import pygame
from FastTetris.colors import Colors


class Grid:
    def __init__(self):
        """Initialize the grid with default values."""
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        """Print the current state of the grid."""
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end=" ")
            print()

    def is_inside(self, row, column):
        """Check if a given cell is inside the grid."""
        return 0 <= row < self.num_rows and 0 <= column < self.num_cols

    def is_empty(self, row, column):
        """Check if a given cell is empty."""
        return self.grid[row][column] == 0

    def is_row_full(self, row):
        """Check if a given row is completely filled."""
        return all(self.grid[row])

    def clear_row(self, row):
        """Clear a given row."""
        self.grid[row] = [0] * self.num_cols

    def move_row_down(self, row, num_rows):
        """Move a row down by a given number of rows."""
        self.grid[row + num_rows] = self.grid[row]
        self.grid[row] = [0] * self.num_cols

    def clear_full_rows(self):
        """Clear all full rows and move rows above them down."""
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def calculate_holes(self):
        """Calculate the number of holes in the grid."""
        holes = 0
        for col in range(self.num_cols):
            for row in range(self.num_rows - 1):
                if self.is_empty(row, col) and not self.is_empty(row + 1, col):
                    holes += 1
        return holes

    def calculate_blockades(self):
        """Calculate the number of blockades in the grid."""
        blockades = 0
        for col in range(self.num_cols):
            for row in range(self.num_rows - 1):
                if not self.is_empty(row, col) and self.is_empty(row + 1, col):
                    blockades += 1
        return blockades

    def calculate_height(self):
        """Calculate the height of the highest column in the grid."""
        heights = [0] * self.num_cols
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                if not self.is_empty(row, col):
                    heights[col] = self.num_rows - row
                    break
        return max(heights)

    def reset(self):
        """Reset the grid to its initial state."""
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]

    def is_grid_full(self):
        """Check if the grid is completely filled."""
        return self.calculate_height() >= self.num_rows

    def copy(self):
        """Create a deep copy of the grid."""
        copied_grid = Grid()
        copied_grid.num_rows = self.num_rows
        copied_grid.num_cols = self.num_cols
        copied_grid.cell_size = self.cell_size
        copied_grid.colors = self.colors
        copied_grid.grid = [row[:] for row in self.grid]
        return copied_grid

    def draw(self, screen):
        """Draw the grid on the screen."""
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column * self.cell_size + 11, row * self.cell_size + 11,
                                        self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
