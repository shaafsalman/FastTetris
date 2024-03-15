import pygame
from colors import Colors


class Grid(object):
    def __init__(self):
        self.rows = 20
        self.cols = 10
        self.cell_size = 30
        self.colors = Colors.get_cell_colors()

        self.grid = [[0 for j in range(self.cols)] for i in range(self.rows)]

    def print_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.grid[row][col], end=" ")
            print()

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = self.grid[row][col]
                cell_rect = pygame.rect.Rect(col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 1,
                                             self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False
