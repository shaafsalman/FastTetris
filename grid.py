import pygame
from colors import Colors


class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 9
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end=" ")
            print()

    def is_inside(self, row, column):
        if 0 <= row < self.num_rows and 0 <= column < self.num_cols:
            return True
        return False

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def calculate_holes(self):
        """
        Calculates the number of holes in the grid.
        A hole is an empty cell with a non-empty cell above it.
        """
        holes = 0
        for col in range(self.num_cols):
            for row in range(self.num_rows - 1):
                if self.is_empty(row, col) and not self.is_empty(row + 1, col):
                    holes += 1
        return holes

    def calculate_blockades(self):
        """
        Calculates the number of blockades in the grid.
        A blockade is a non-empty cell with an empty cell below it.
        """
        blockades = 0
        for col in range(self.num_cols):
            for row in range(self.num_rows - 1):
                if not self.is_empty(row, col) and self.is_empty(row + 1, col):
                    blockades += 1
        return blockades

    def calculate_height(self):
        """
        Calculates the height of the highest column in the grid.
        """
        heights = [0] * self.num_cols
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                if not self.is_empty(row, col):
                    heights[col] = self.num_rows - row
                    break
        return max(heights)

    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def is_grid_full(self):
        return self.calculate_height() >= self.num_rows

    def copy(self):
        copied_grid = Grid()
        copied_grid.num_rows = self.num_rows
        copied_grid.num_cols = self.num_cols
        copied_grid.cell_size = self.cell_size
        copied_grid.colors = self.colors

        # Copy the values from the original grid to the new grid
        copied_grid.grid = [row[:] for row in self.grid]

        return copied_grid

    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column * self.cell_size + 11, row * self.cell_size + 11,
                                        self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

    def can_place_block(self, block, row, col):
        """
        Checks if the given block can be placed at the specified row and column in the grid.
        Returns True if the block can be placed, False otherwise.
        """
        for position in block.get_cell_positions():
            if not self.is_inside(row + position.row, col + position.column):
                return False
            if not self.is_empty(row + position.row, col + position.column):
                return False
        return True
