class Player:
    def __init__(self, name):
        self.move_history = []
        self.name = name

    def set_move_history(self, move):
        self.move_history.append(move)
