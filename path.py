class Path:
    def __init__(self):
        self.moves = []
        self.height = 0
        self.lines_cleared = 0
        self.holes = 0
        self.blockades = 0
        self.game_over_move = False
        self.rank = 0

    def set_moves(self, moves):
        self.moves = moves

    def set_attributes(self, height, lines_cleared, holes, blockades):
        self.height = height
        self.lines_cleared = lines_cleared
        self.holes = holes
        self.blockades = blockades

    def set_rank(self, rank):
        self.rank = rank

    def set_game_over_move(self, game_over_move):
        self.game_over_move = game_over_move

    def set_path(self, moves, height, lines_cleared, holes, blockades, game_over_move):
        self.moves = moves
        self.height = height
        self.lines_cleared = lines_cleared
        self.holes = holes
        self.blockades = blockades
        self.game_over_move = game_over_move

    def print_details(self):
        print("Moves:", self.moves)
        print("Height:", self.height)
        print("Lines Cleared:", self.lines_cleared)
        print("Holes:", self.holes)
        print("Blockades:", self.blockades)
        print("Rank:", self.rank)
        print("Game Over Move:", self.game_over_move)
