import sys
from player import Player


class Player(Player):
    def decide(self, game, state, available_moves, opponent_moves):
        condition = True
        move = None

        while condition:
            user_input = input().split(' ')

            if len(user_input) != 3:
                print('Incorrect format. Example: "3 2 2"')
                continue

            x, y, shift = [int(el) for el in user_input]

            move = game.create_move(state, x, y, shift)

            condition = False if move else True

            if condition:
                print('This is not a legal move. Try again')

        return [
            move.row,
            move.column,
            move.shift
        ]
