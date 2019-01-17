import sys
from player import Player
import collections
import numpy as np

class Player(Player):
	def decide(self, game, state, available_moves, opponent_moves):
		condition = True
		move = None

		while condition:
			print("Evaluation for %d:" % state.current_player, self.evaluate(state))
			# rowcol = max([collections.Counter(row).get(1, 0) for row in state.board] + [collections.Counter(row).get(1, 0)
			# 																	   for row in state.board.transpose()])
			# # print(max([collections.Counter(row).get(1, 0) for row in state.board] + [collections.Counter(row).get(1, 0)
			# # 																	   for row in state.board.transpose()]))
			# Y = state.board[:, ::-1]
			#
			# diagonals = [np.diagonal(state.board), np.diagonal(Y)]
			# print(max(rowcol, max(collections.Counter(diagonals[0]).get(1, 0), collections.Counter(diagonals[1]).get(1, 0))))


			# print(max(collections.Counter(diagonals[0]).get(1, 0), collections.Counter(diagonals[1]).get(1, 0)))
			# diagonal = [[], []]
			# diagonal[0].append([state.board[i:i] for i in range(game.rows)])


			# print(state.board[:, :])
			# print("max 1 count in rows:", max([row.count(1) for row in state.board]))
			# print("Utility score for player (o) in rows:", max([collections.Counter(row).get(1, 0) for row in state.board]))
			# trans = state.board.transpose()
			# print("Utility score for player (o) in columns:",max([collections.Counter(column).get(1, 0) for column in trans]))
			# print("max 1 count in columns:", max([column.count(1)] for column in trans))
			# for column in state.board.transpose():
			# 	print(column)




			# rws, clmns = [], []
			# print(state.board)
			# for i in range(game.rows):
			# 	rws.append([state.board[i,j] for j in range(game.columns)].count(1))
			# 	print("-1 in row", i, [state.board[i,j] for j in range(game.columns)].count(-1))
			# print(max(rws))
			# for j in range(game.columns):
			# 	print("1 in column", j, [state.board[i,j] for i in range(game.rows)].count(1))
			# 	print("-1 in column", j, [state.board[i,j] for i in range(game.rows)].count(-1))
			user_input = input().split(' ')

			if len(user_input) != 3:
				print('Incorrect format. Example: "3 2 2"')
				continue

			x, y, shift = [int(el) for el in user_input]

			move = game.create_move(state, x, y, shift)

			condition = False if move else True

			if condition:
				print('This is not a legal move. Try again')

		return [move.row, move.column,move.shift]

	def evaluate(self, state):
		rowcol = max([collections.Counter(row).get(state.current_player, 0) for row in state.board] + [collections.Counter(row).get(state.current_player, 0)
																					for row in state.board.transpose()])
		Y = state.board[:, ::-1]
		diagonals = [np.diagonal(state.board), np.diagonal(Y)]
		# max(max([collections.Counter(row).get(1, 0) for row in state.board] + [collections.Counter(row).get(1, 0) for row in
		# 																   state.board]), max(collections.Counter(diagonals[0]).get(1, 0), collections.Counter(diagonals[1]).get(1, 0)))
		return max(rowcol, max(collections.Counter(diagonals[0]).get(state.current_player, 0), collections.Counter(diagonals[1]).get(state.current_player, 0)))

