from player import Player
from random import randint


class Player(Player):
    def decide(self, game, state, available_moves, opponent_moves):
        index = randint(0, len(available_moves) - 1)
        move = available_moves[index]

        return [move.row, move.column, move.shift]
