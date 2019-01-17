from quixo import Quixo
from match import Match
import numpy as np

game = Quixo(5, 5)

state = game.initial_state()

match = Match(game, state, 20)

match.set_players()

match.start()
#
# count = 100
# wincount = [0, 0]
# draw = 0
# for i in range(count):
# 	game = Quixo(5, 5)
#
# 	state = game.initial_state()
#
# 	match = Match(game, state, 20)
# 	match.playersvs("random", "random")
# 	match.start()
