class Chomp:
    def __init__(self):
        self.width = 5
        self.height = 4
        self.board = []
        self.chocolate = 1
        self.poisoned_chocolate = 2
        self.empty_place = 0
        self.game_running = False
        self.player_1_turn = True
    
    def start_game(self, starts_first):
        self.board = [[self.chocolate for _ in range(self.width)] for _ in range(self.height)]
        self.board[0][0] = self.poisoned_chocolate
        self.game_running = True
        self.player_1_turn = starts_first
        
    def eat_chocolate(self, x, y):
        if not self.game_running:
            return False
            
        self.board = [
            [self.empty_place if (i >= y and j >= x) else self.board[i][j]
                for j in range(self.width)]
            for i in range(self.height)
        ]
        
        lost = self.board[0][0] == self.empty_place
        if lost:
            self.game_running = False
            return True
            
        self.player_1_turn = not self.player_1_turn
        return False

