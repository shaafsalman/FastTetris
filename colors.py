class Colors:
    # Define colors for Tetris blocks
    grid_clr = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    orange = (255, 140, 0)
    yellow = (255, 255, 0)
    purple = (128, 0, 128)
    cyan = (0, 255, 255)
    blue = (0, 0, 255)

    # Define additional colors
    white = (255, 255, 255)
    dark_blue = (0, 0, 128)
    light_blue = (135, 206, 235)

    BACKGROUND_COLOR = (23, 32, 42)   # Background color for the game
    ACCENT_COLOR = (127, 219, 255)    # Accent color
    TEXT_COLOR = (236, 240, 241)      # Text color
    GAME_OVER_COLOR = (231, 76, 60)   # Color for game over screen

    @classmethod
    def get_cell_colors(cls):
        """
        Get a list of colors for Tetris blocks.

        Returns:
            list: A list of colors for Tetris blocks.
        """
        return [cls.grid_clr, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
