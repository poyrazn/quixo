import sys
from player import Player


class Player(Player):
    def __init__(self, name):
        super().__init__(name)

        self.name = 'Nehir'

    def decide(self, game, state, available_moves, opponent_moves):
        # This student wants to to play the same move everytime
        return [0, 0, 2]
