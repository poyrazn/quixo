import os
import sys
import time
import pydoc


class Match:
	def __init__(self, game, state, timeout):
		self.game = game
		self.state = state
		self.players = {}
		self.timeout = timeout


	def playersvs(self, player1, player2):
		players = [player1, player2]
		player_classes = [pydoc.locate('players.' + player) for player in players]
		players = [player.Player(players[index]) for index, player in enumerate(player_classes)]
		self.players = {1: players[0], -1: players[1]}

	def set_players(self):
		players = []
		player_classes = []
		incorrect_input = True

		while incorrect_input:
			players = input('\nWho are the players?\n(Example: "manual random")\n')
			players = players.split(' ')

			if len(players) != 2:
				print('!-- Incorrect number of players --!')
				continue

			player_classes = [pydoc.locate('players.' + player) for player in players]
			incorrect_class = False

			for index, player in enumerate(player_classes):
				if player is None:
					incorrect_class = True
					print('!-- The player "' + players[index] + '" does not exist --!')

			if incorrect_class:
				continue

			incorrect_input = False

		players = [player.Player(players[index]) for index, player in enumerate(player_classes)]

		self.players = {1: players[0], -1: players[1]}

	def start(self):
		print('\nPlayer1: ' + str(self.players[1].name) + ' (o)')
		print('Player2: ' + str(self.players[-1].name) + ' (x)\n')

		# for i in range(5, 0, -1):
		#     sys.stdout.write('\rStarting in ' + str(i) + ' seconds')
		#     sys.stdout.flush()
		#     time.sleep(1)
		# print('\n')

		turns = 0
		while True:
			print('\nTurn: ' + self.players[self.state.current_player].name + ' (' + ('o' if self.state.current_player == 1 else 'x') + ')')

			self.game.print_board(self.state)

			move = self.get_player_move()

			print(move)

			self.players[self.state.current_player].set_move_history(move)

			self.state = self.game.apply_move(self.state, move)

			turns += 1

			if self.state.winner:
				break

		print('\n\n!!! GAME ENDED !!!\n\n')

		self.game.print_board(self.state)

		if self.state.winner == 'Draw':
			print('\nDraw.')
		else:
			print(
				'\nWinner: ' +
				self.players[self.state.winner].name +
				' (' +
				('o' if self.state.winner == 1 else 'x') +
				')'
				)

		print('\nNumber of turns: ' + str(turns))

	def get_player_move(self):
		row, column, shift = self.players[self.state.current_player].decide(
			self.game,
			self.state,
			self.game.get_moves(self.state),
			self.players[self.state.current_player * -1].move_history
		)

		move = self.game.create_move(self.state, row, column, shift, False)

		if move == False:
			print('The player "'
				  + self.players[self.state.current_player].name
				  + '" made an incorrect move. \nThe move was: ' + str((row, column, shift)))
			exit()

		return move
