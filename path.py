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

    def set_weights(self, height_weight, lines_cleared_weight, holes_weight, blockades_weight):
        self.height_weight = height_weight
        self.lines_cleared_weight = lines_cleared_weight
        self.holes_weight = holes_weight
        self.blockades_weight = blockades_weight

    def set_rank(self, rank):
        self.rank = rank

    def set_game_over_move(self, game_over_move):
        self.game_over_move = game_over_move

    def set_path(self, moves, height_weight, lines_cleared_weight, holes_weight, blockades_weight, game_over_move):
        self.moves = moves
        self.height_weight = height_weight
        self.lines_cleared_weight = lines_cleared_weight
        self.holes_weight = holes_weight
        self.blockades_weight = blockades_weight
        self.game_over_move = game_over_move
