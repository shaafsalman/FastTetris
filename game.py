import os

from grid import Grid
from all_blocks import *
import random
import pygame


def load_highest_score():
    if os.path.exists("assets/highest_score.txt"):
        with open("assets/highest_score.txt", "r") as file:
            content = file.read().strip()
            if content.isdigit():

                return int(content)
            else:
                print("Error: Highest score file contains invalid content.")
                return 0
    else:
        return 0


def save_highest_score(self):
    with open("assets/highest_score.txt", "w") as file:
        file.write(str(self.highest_score))


def calculate_holes(grid):
    """
    Calculates the number of holes in the grid.
    """
    holes = 0
    for col in range(grid.num_cols):
        for row in range(grid.num_rows - 1):
            if grid.is_empty(row, col) and not grid.is_empty(row + 1, col):
                holes += 1
    return holes


def calculate_all_holes(grid):
    """
    Calculates the number of minor, major, and absolute holes in the grid.
    """
    minor_holes = 0
    major_holes = 0
    absolute_holes = 0

    for col in range(grid.num_cols):
        topmost_filled_row = None
        for row in range(grid.num_rows):
            if not grid.is_empty(row, col):
                topmost_filled_row = row
                break

        if topmost_filled_row is not None:
            for row in range(topmost_filled_row):
                if grid.is_empty(row, col):
                    if col == 0 or not grid.is_empty(row, col - 1):
                        minor_holes += 1

            for row in range(topmost_filled_row + 1, grid.num_rows):
                if grid.is_empty(row, col):
                    if col == 0 or not grid.is_empty(row, col - 1):
                        absolute_holes += 1

            if topmost_filled_row < grid.num_rows - 1 and grid.is_empty(topmost_filled_row + 1, col):
                major_holes += 1

    return minor_holes, major_holes, absolute_holes


def count_complete_rows(grid):
    """
    Counts the number of complete rows in the grid.
    """
    complete_rows = 0

    for row in range(grid.num_rows):
        is_complete = all(grid[row][col] != 0 for col in range(grid.num_cols))
        if is_complete:
            complete_rows += 1

    return complete_rows


def calculate_blockades(grid):
    """
    Calculates the number of blockades in the grid.
    """
    blockades = 0
    for col in range(grid.num_cols):
        for row in range(grid.num_rows - 1):
            if not grid.is_empty(row, col) and grid.is_empty(row + 1, col):
                blockades += 1
    return blockades


def calculate_height(grid):
    """
    Calculates the height of the highest column in the grid.
    """
    heights = [0] * grid.num_cols
    for col in range(grid.num_cols):
        for row in range(grid.num_rows):
            if not grid.is_empty(row, col):
                heights[col] = grid.num_rows - row
                break
    return max(heights)


def turn_off_music():
    """Turns off all music."""
    pygame.mixer.music.stop()


class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.lines = 0
        self.highest_score = load_highest_score()

        self.lines_cleared = 0

        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

        pygame.mixer.music.load("Sounds/music.ogg")
        # pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points
        if self.score > self.highest_score:
            self.highest_score = self.score
            save_highest_score(self)

    def update_numer_of_lines(self, lines_cleared):
        self.lines += lines_cleared

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()
            return True

    def lock_block(self):
        # print("Lock Block Called")
        # self.grid.print_grid()
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
            self.lines_cleared += rows_cleared
            self.update_numer_of_lines(rows_cleared)
        if not self.block_fits():
            self.game_over = True
        return rows_cleared

    def lock_block2(self):
        # print("Lock Block Called")
        # self.grid.print_grid()
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id

        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
            self.lines_cleared += rows_cleared
            self.update_numer_of_lines(rows_cleared)
        if not self.block_fits():
            self.game_over = True
        return rows_cleared


    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        # else:
        #     # self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        # Draw the next block
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)

    def check_collision(self):
        """
        Checks if the current block collides with any existing blocks in the grid.
        """
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return True
        return False

    def block_at_bottom(self):
        """
        Checks if the current block is at the bottom of the grid.
        """
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if tile.row == self.grid.num_rows - 1:
                return True
        return False

    def copy(self):
        copied_game = Game()
        copied_game.grid = self.grid.copy()
        copied_game.blocks = [block.copy() for block in self.blocks]
        copied_game.current_block = self.current_block.copy()
        copied_game.next_block = self.next_block.copy()
        copied_game.game_over = self.game_over
        copied_game.score = self.score
        copied_game.lines = self.lines
        copied_game.highest_score = self.highest_score

        return copied_game

    def apply_moves_to_grid(self, path):
        holes = 0
        blockades = 0
        full_rows = 0
        max_height = 0
        minor_holes = 0
        major_holes = 0
        absolute_holes = 0
        print("checking move before grid:")
        print(path)
        self.current_block.print_details()

        self.grid.print_grid()

        attached = False

        # grid_copy = self.grid.copy()

        for move in path:
            if move == "ROTATE":
                self.rotate()
            elif move == "LEFT":
                self.move_left()
            elif move == "RIGHT":
                self.move_right()
            elif move == "DOWN":
                # attached = self.move_down()
                self.current_block.move(1, 0)
                if not self.block_fits():
                    attached = True
                    self.current_block.move(-1, 0)
                    full_rows = self.lock_block2()

            if self.check_collision() or self.block_at_bottom() or attached:
                print("Final Grid")
                self.grid.print_grid()
                self.lock_block()
                # holes = self.calculate_holes(self.grid)
                blockades = calculate_blockades(self.grid)
                full_rows = self.lines_cleared
                max_height = calculate_height(self.grid)

                minor_holes, major_holes, absolute_holes = calculate_all_holes(self.grid)

                print("minor_holes, major_holes, absolute_holes")
                print(minor_holes, ",", major_holes, ",", absolute_holes)

                print("max height", max_height)
                print("Holes", absolute_holes)
                print("Full Lines", full_rows)
                print("Blockades", blockades)
                break
        # time.sleep(2)
        total_holes = minor_holes + 2 * major_holes * 4 * absolute_holes
        return total_holes, blockades, full_rows, max_height
