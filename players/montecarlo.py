from player import Player
from mittmcts import MCTS

class Player(Player):
    def decide(self, game, state, available_moves, opponent_moves, stdin, result):
        result = MCTS(game, state).get_simulation_result(1000)
        move = result.move

        return move
