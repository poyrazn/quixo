#
# ogrencikodu
# quixo
#
# Created by Nehir Poyraz on 18.01.2019
# Copyright 2019 Nehir Poyraz. All rights reserved.


from player import Player
import collections
import numpy as np
import copy

class Player(Player):
	def __init__(self, name):
		super().__init__(name)

		self.name = 'Nehir'
		self.move = None

	def decide(self, game, state, available_moves, opponent_moves):
		# This student wants to to play the same move everytime
		statecopy = copy.deepcopy(state)
		root = GameNode(game, None, statecopy, available_moves, None)
		tree = GameTree(root)
		minimaxAB = AlphaBeta(tree)
		best_state = minimaxAB.alpha_beta_search(tree.root)
		move = best_state.action
		return [move.row, move.column, move.shift]



class GameNode:
	def __init__(self, game, action, state, available_moves, parent=None):
		self.Game = game
		self.State = state      # a char
		self.value = self.evaluate(self.State)
		self.parent = parent  # a node reference
		self.moves = available_moves
		self.children = []    # a list of nodes
		self.action = action

	def addChild(self, childNode):
		self.children.append(childNode)

	def expand(self):
		for move in self.moves:
			m = self.Game.create_move(self.State, move.row, move.column, move.shift, False)
			childstate = self.Game.apply_move(copy.deepcopy(self.State), m)
			child = GameNode(self.Game, m, childstate, self.Game.get_moves(childstate), self)
			self.addChild(child)


	def evaluate(self, state):
		transpose = state.board.transpose()
		count = []
		opponentcount = []
		for row, column in zip(state.board, transpose):
			rowcounter = collections.Counter(row)
			columncounter = collections.Counter(column)
			count.append(rowcounter.get(state.current_player, 0))
			count.append(columncounter.get(state.current_player, 0))
			opponentcount.append(rowcounter.get(state.current_player * - 1, 0))
			opponentcount.append(columncounter.get(state.current_player * -1 , 0))

		Y = state.board[:, ::-1]
		diagonals = [np.diagonal(state.board), np.diagonal(Y)]
		main_diagonal_count = collections.Counter(diagonals[0])
		second_diagonal_count = collections.Counter(diagonals[1])
		count.append(main_diagonal_count.get(state.current_player, 0))
		count.append(second_diagonal_count.get(state.current_player, 0))
		opponentcount.append(main_diagonal_count.get(state.current_player * - 1, 0))
		opponentcount.append(second_diagonal_count.get(state.current_player * -1, 0))

		scoremax = 5 ** max(count)
		scoremin = 5 ** max(opponentcount)

		return scoremax - scoremin



class GameTree:
	def __init__(self, root):
		self.root = root
		current = root
		current.expand()
		if len(current.children) > 0:
			for child in current.children:
				child.expand()




class AlphaBeta:
	def __init__(self, game_tree):
		self.game_tree = game_tree  # GameTree
		self.root = game_tree.root  # GameNode
		return

	def alpha_beta_search(self, node):
		infinity = float('inf')
		best_val = -infinity
		beta = infinity

		successors = self.getSuccessors(node)
		best_state = None
		for state in successors:
			value = self.min_value(state, best_val, beta)
			if value > best_val:
				best_val = value
				best_state = state
		return best_state

	def max_value(self, node, alpha, beta):
		if self.isTerminal(node):
			return self.getUtility(node)
		infinity = float('inf')
		value = -infinity

		successors = self.getSuccessors(node)
		for state in successors:
			value = max(value, self.min_value(state, alpha, beta))
			if value >= beta:
				return value
			alpha = max(alpha, value)
		return value

	def min_value(self, node, alpha, beta):
		if self.isTerminal(node):
			return self.getUtility(node)
		infinity = float('inf')
		value = infinity

		successors = self.getSuccessors(node)
		for state in successors:
			value = min(value, self.max_value(state, alpha, beta))
			if value <= alpha:
				return value
			beta = min(beta, value)

		return value


	# successor states in a game tree are the child nodes...
	def getSuccessors(self, node):
		assert node is not None
		return node.children


	# return true if the node has NO children (successor states)
	# return false if the node has children (successor states)
	def isTerminal(self, node):
		assert node is not None
		return len(node.children) == 0


	def getUtility(self, node):
		assert node is not None
		return node.value
