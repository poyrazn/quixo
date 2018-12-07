import numpy as np
from collections import namedtuple
from copy import deepcopy

edge_blocks = np.array([(0, i) for i in range(3)] +
                                    [(2, i) for i in range(3)] +
                                    [(i, 0) for i in range(1, 2)] +
                                    [(i, 2) for i in range(1, 2)])

boundary_xs, boundary_ys = edge_blocks.T

class Quixo:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def initial_state(self):
        return State(np.zeros((self.rows, self.columns), dtype=np.int), 1, None)

    def apply_move(self, state, move):
        state.board[move.row, move.column] = state.current_player

        if move.shift == 0:
            state.board[:, move.column] = np.concatenate([
                np.roll(state.board[:, move.column][:move.row + 1], shift = 1),
                state.board[:, move.column][move.row + 1:]
                ])
        elif move.shift == 1:
            state.board[move.row] = np.concatenate([
                np.roll(state.board[move.row][:move.column + 1], shift = 1),
                state.board[move.row][move.column + 1:]
                ])
        elif move.shift == 2:
            state.board[:, move.column] = np.concatenate([
                state.board[:, move.column][:move.row],
                np.roll(state.board[:, move.column][move.row:], shift = -1)
                ])
        else:
            state.board[move.row] = np.concatenate([
                state.board[move.row][:move.column],
                np.roll(state.board[move.row][move.column:], shift = -1)
                ])

        winner = self.determine_winner(state.board) if self.check_for_winner(state.board) else None

        return State(
            state.board,
            state.current_player * -1,
            winner
            )

    def get_moves(self, state):
        moves = []
        for row_index, row in enumerate(state.board):
            for column_index, value in enumerate(row):
                for i in range(0, 5):
                    move = self.create_move(state, row_index, column_index, i, False)
                    if (move != False):
                        moves.append(move)

        return moves

    def check_for_winner(self, board):
        return (
            any(abs(np.sum(board, axis = 0)) == self.rows) or
            any(abs(np.sum(board, axis = 1)) == self.columns) or
            (
                self.rows == self.columns and
                (
                    abs(np.sum((board.diagonal()))) == min(self.rows, self.columns) or
                    abs(np.sum((board[::-1].diagonal()))) == min(self.rows, self.columns)
                )
            )
            )

    def determine_winner(self, board):
        winning_players = []

        row_sums = np.sum(board, axis = 0)
        win_rows = np.where(np.abs(row_sums) == self.rows)[0]

        if (len(win_rows) > 0):
            winning_players.extend(np.sign(row_sums[win_rows]))

        col_sums = np.sum(board, axis = 1)
        win_cols = np.where(np.abs(col_sums) == self.columns)[0]

        if (len(win_cols) > 0):
            winning_players.extend(np.sign(col_sums[win_cols]))

        if (self.rows == self.columns):
            diag0 = np.sum((board.diagonal()))
            diag1 = np.sum((board[::-1].diagonal()))

            for diag in [diag0, diag1]:
                if (abs(diag) == self.rows):
                    winning_players.append(np.sign(diag))

        winning_players = list(set(winning_players))

        if len(winning_players) > 1:
            return 'Draw'
        else:
            return winning_players[0]

    def print_board(self, state):
        char_map = np.array([' ', 'o', 'x'])

        print('  ' + ' '.join(map(str, np.arange(self.columns))) +
              '\n' + '_' * (self.columns * 2 + 2))

        for row_index, row in enumerate(state.board):
            print(str(row_index) + '|' + '|'.join(char_map[row]) + '|')

        print('_' * (self.columns * 2 + 2))

    def create_move(self, state, row, column, shift, log = True):
        if state.board[row][column] == state.current_player * -1:
            if log:
                print('Opponents pieces cannot be moved')
            return False

        if (row not in [0, self.rows - 1] and
                column not in [0, self.columns - 1]):
            if (log): print('Only the pieces on the sides can be moved')
            return False

        if ((row == 0 and shift == 0) or
                (column == 0 and shift == 1) or
                (row == self.rows - 1 and shift == 2) or
                (column == self.columns - 1 and shift == 3)):
            if (log): print('You cannot shift (' + str(row) + ',' + str(column) + ') with ' + str(shift))
            return False

        if shift not in [0, 1, 2, 3]:
            if (log): print('Incorrect shift paramter.\n' +
                'Shifting options: 0(TOP), 1(LEFT), 2(BOTTOM), 3(RIGHT)')
            return False

        return Move(row, column, shift)

class Move:
    def __init__(self, row, column, shift):
        self.row = row
        self.column = column
        self.shift = shift

    def __str__(self):
        return '(' + str(self.row) + ',' + str(self.column) + ',' + str(self.shift) + ')'

class State:
    def __init__(self, board, current_player, winner):
        self.board = board
        self.current_player = current_player
        self.winner = winner
