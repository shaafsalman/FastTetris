

class Grid(object):
    def __init__(self):
        self.rows = 20
        self.cols = 10
        self.cell_size = 30


        self.grid = [[0 for j in range(self.cols)] for i in range(self.rows)]

    def printGrid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.grid[row][col], end = " ")
            print()


    def get_cell_colors(self):
        dark_grey = (26, 31, 40)
        green = (47, 230, 23)
        red = (232, 18, 18)
        orange = (226, 116, 17)
        yellow = (237, 234, 3)
        purple = (166, 0, 247)
        cyan = (21, 204, 209)
        blue = (13, 64, 216)

