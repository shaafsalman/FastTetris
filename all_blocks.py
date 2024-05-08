from FastTetris.block import Block
from position import Position

"""
   Classes of blocks inherited from Block we set name number of rotations and move it to
   needed position set as their origin of spawn like in this very case they are spawned at
   the left top corner of the grid.
"""


class LBlock(Block):
    """
    Class representing the L-shaped Tetris block.
    """

    def __init__(self):
        super().__init__(id=1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        self.name = "L"
        self.num_rotations = 4
        self.move(0, 3)


class JBlock(Block):
    """
    Class representing the J-shaped Tetris block.
    """

    def __init__(self):
        super().__init__(id=2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.name = "J"
        self.num_rotations = 4
        self.move(0, 3)


class IBlock(Block):
    """
    Class representing the I-shaped Tetris block.
    """

    def __init__(self):
        super().__init__(id=3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.name = "I"
        self.num_rotations = 4
        self.move(-1, 0)


class OBlock(Block):
    """
    Class representing the O-shaped Tetris block.
    """

    def __init__(self):
        super().__init__(id=4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
        }
        self.name = "O"
        self.num_rotations = 1
        self.move(0, 4)


class SBlock(Block):
    """
    Class representing the S-shaped Tetris block.
    """

    def __init__(self):
        super().__init__(id=5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.name = "S"
        self.num_rotations = 4
        self.move(0, 0)


class TBlock(Block):
    """
    Class representing the T-shaped Tetris block.
    """

    def __init__(self):
        super().__init__(id=6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.name = "T"
        self.num_rotations = 4
        self.move(0, 0)


class ZBlock(Block):
    """
    Class representing the Z-shaped Tetris block.
    """

    def __init__(self):
        super().__init__(id=7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        self.name = "Z"
        self.num_rotations = 4
        self.move(0, 0)


def main():
    # Create instances of each Tetris block
    l_block = LBlock()
    j_block = JBlock()
    i_block = IBlock()
    o_block = OBlock()
    s_block = SBlock()
    t_block = TBlock()
    z_block = ZBlock()

    print("L Block Details:")
    l_block.print_details()
    print("\nJ Block Details:")
    j_block.print_details()
    print("\nI Block Details:")
    i_block.print_details()
    print("\nO Block Details:")
    o_block.print_details()
    print("\nS Block Details:")
    s_block.print_details()
    print("\nT Block Details:")
    t_block.print_details()
    print("\nZ Block Details:")
    z_block.print_details()


if __name__ == "__main__":
    main()
