class Colors:
    grid_clr =	(0,0,0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    orange = (255, 140, 0)
    yellow = (255, 255, 0)
    purple = (128, 0, 128)
    cyan = (0, 255, 255)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    dark_blue = (0, 0, 128)
    light_blue = (135, 206, 235)

    BACKGROUND_COLOR = (23, 32, 42)
    ACCENT_COLOR = (127, 219, 255)
    TEXT_COLOR = (236, 240, 241)
    GAME_OVER_COLOR = (231, 76, 60)

    @classmethod
    def get_cell_colors(cls):
        return [cls.grid_clr, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
