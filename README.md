# Quixo Game
This project focuses on Quixo Game and an AI Quixo player. 
The agent is modelled using minimax algorithm with alpha-beta pruning.

Quixo is designed by Thierry Chapeau and currently published by Gigamic Games.
The goal is to arrange 5 tiles in a row vertically, horizontally or diagonally.

For more information and rules about the game: https://en.gigamic.com/game/quixo

# Quixo Gameplay on Computer

Developed by a classmate. 

If one of the specified players is `manual`, this means a user input will be requested.
User inputs must follow this format:
    `<row-no> <column-no> <shift-direction>`
Example:
    `1 3 1`
    `4 1 0`
    `2 4 3`
    `0 4 2`

ABOUT SHIFT DIRECTION PARAMETER
-------------------------------
0 -> Place the piece to the board from the top side
1 -> Place the piece to the board from the left side
2 -> Place the piece to the board from the bottom side
3 -> Place the piece to the board from the right side


# AI Quixo Player

AI player for Quixo game is developed using minimax algorithm with alpha-beta pruning.

Where minimax is used to create a game tree and assess the game to decide on the best move, alpha-beta search is used to decrease the number of nodes that are evaluated by minimax in its search tree.



