from FastTetris.colors import Colors
import pygame
from position import Position


class Block:
    def __init__(self, id):
        """
        Initialize a Block object.

        Args:
            id (int): The unique identifier for the block.
        """
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.number_of_rotations = 0
        self.name = ""
        self.colors = Colors.get_cell_colors()

    def move(self, rows, columns):
        """
        Move the block by the specified number of rows and columns.

        Args:
            rows (int): The number of rows to move the block.
            columns (int): The number of columns to move the block.
        """
        self.row_offset += rows
        self.column_offset += columns
        self.number_of_rotations = len(self.cells)

    def get_cell_positions(self):
        """
        Get the positions of all cells in the current rotation state.

        Returns:
            list: A list of Position objects representing the cell positions.
        """
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    def rotate(self):
        """
        Rotate the block clockwise by 90 degrees.
        """
        self.rotation_state = (self.rotation_state + 1) % len(self.cells)

    def undo_rotation(self):
        """
        Undo the previous rotation of the block.
        """
        self.rotation_state = (self.rotation_state - 1) % len(self.cells)

    def draw(self, screen, offset_x, offset_y):
        """
        Draw the block on the screen.

        Args:
            screen: The pygame surface to draw the block on.
            offset_x (int): The x-coordinate offset for drawing the block.
            offset_y (int): The y-coordinate offset for drawing the block.
        """
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size,
                                    offset_y + tile.row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    def print_details(self):
        """
        Print details about the block.
        """
        print(f"Block ID: {self.id}")
        print(f"Block Name: {self.name}")
        print(f"Cell Size: {self.cell_size}")
        print(f"Row Offset: {self.row_offset}")
        print(f"Column Offset: {self.column_offset}")
        print(f"Rotation State: {self.rotation_state}")
        print(f"Number of Rotations: {self.number_of_rotations}")
        print("Cell Positions:")

    def calculate_dimensions(self):
        """
        Calculate the width and height of the block.

        Returns:
            tuple: A tuple containing the width and height of the block.
        """
        min_row, max_row, min_col, max_col = float('inf'), float('-inf'), float('inf'), float('-inf')
        for rotation in self.cells.values():
            for position in rotation:
                min_row = min(min_row, position.row)
                max_row = max(max_row, position.row)
                min_col = min(min_col, position.column)
                max_col = max(max_col, position.column)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        return width, height

    def copy(self):
        """
        Create a copy of the block.

        Returns:
            Block: A copy of the block.
        """
        copied_block = Block(self.id)
        copied_block.cells = {key: value[:] for key, value in self.cells.items()}
        copied_block.cell_size = self.cell_size
        copied_block.row_offset = self.row_offset
        copied_block.column_offset = self.column_offset
        copied_block.rotation_state = self.rotation_state
        copied_block.colors = self.colors.copy()
        copied_block.name = self.name
        copied_block.number_of_rotations = self.number_of_rotations
        copied_block.width, copied_block.height = self.calculate_dimensions()
        # print("---------------------o----------------")
        # self.print_details()
        # print("---------------------c----------------")
        # copied_block.print_details()
        return copied_block
