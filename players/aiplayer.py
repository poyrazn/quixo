#
# aiplayer
# quixo
#
# Created by Nehir Poyraz on 18.01.2019


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
		"""

		This method returns a Move that the player decides

		:param game: Quixo object (fn calls)
		:param state: State object (attr: board, current_player, winner)
		:param available_moves: a list of Move objects (Move attr: row, column, shift)
		:param opponent_moves: a list of Move objects (Move attr: row, column, shift)
		:return: decided Move

		First a GameNode is created with given parameters, then a GameTree with the root being the recently created node.
		The tree is then searched to find the best state the agent can be in using minimax search with alpha-beta pruning technique.
		The move is decided as the action that leads to the best state.

		"""
		statecopy = copy.deepcopy(state)
		root = GameNode(game, None, statecopy, available_moves, None)
		tree = GameTree(root)
		minimaxAB = AlphaBeta(tree)
		best_state = minimaxAB.alpha_beta_search(tree.root)
		move = best_state.action
		return [move.row, move.column, move.shift]


class GameNode:
	def __init__(self, game, action, state, available_moves, parent=None):
		"""

		:param game: Quixo object (fn calls)
		:param action: the action that leads to this node
		:param state: State object (attr: board, current_player, winner)
		:param available_moves: a list of Move objects (Move attr: row, column, shift)
		:param parent: Parent node of this node
		"""
		self.Game = game
		self.State = state
		self.value = self.evaluate(self.State)
		self.parent = parent  # a node reference
		self.moves = available_moves
		self.children = []    # a list of nodes
		self.action = action

	def addChild(self, childNode):
		if childNode not in self.children:
			self.children.append(childNode)

	def expand(self):
		"""
		expands children of a node (makes available moves in current state and appends resultant states as children)
		:return:
		"""
		for move in self.moves:
			m = self.Game.create_move(self.State, move.row, move.column, move.shift, False)
			childstate = self.Game.apply_move(copy.deepcopy(self.State), m)
			child = GameNode(self.Game, m, childstate, self.Game.get_moves(childstate), self)
			self.addChild(child)

	def evaluate(self, state):
		"""
		Heuristic function for state value, returns a score(int)

		:param state: current state, State object (attr: board, current_player, winner)
		:return: int

		for every row, column and diagonal it counts the number of player's tiles and opponent's tiles and stores in lists.
		score is calculated as
		score = 5^(p) - 5^(o)
		p = max number of player's tiles in a row, column or diagonal (from the search space of every row, column and diagonal)
		o = max num of opponent's tiles in a row, column or diagonal

		this way, it is mostly guaranteed that the player wants to choose states where itself is closer to finish than its opponent.


		"""
		transpose = state.board.transpose()		# columns in state.board = rows in transpose
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

		# max(count): maximum number of player's tiles in a row, column, or a diagonal (the highest value is 5)
		# max(opponentcount): maximum number of opponent's tiles in a row, column, or a diagonal (the highest value is 5)
		scoremax = 5 ** max(count)
		scoremin = 5 ** max(opponentcount)

		return scoremax - scoremin


class GameTree:

	def __init__(self, root):
		"""
		:param root: root node (GameNode)

		constructs a game tree where the root is given
		(expands root and then expands children, generally results in a game tree of height 2 if there are available moves)

		Tree structure (relative to the root): 	(root->children->grandchildren)

		"""
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
		"""
		:param node: current node
		:return: best state (child node)

		min max tree search with alpha-beta pruning assuming the player is maximizing player

		"""
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

	# successor states in a game tree are the child nodes
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
