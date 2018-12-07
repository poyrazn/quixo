from quixo import Quixo
from match import Match
import numpy as np

game = Quixo(3, 3)

state = game.initial_state()

match = Match(game, state, 20)

match.set_players()

match.start()
