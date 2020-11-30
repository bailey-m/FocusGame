# An example of gameplay using the FocusGame library! In this game, Player A wins.
# Feel free to download and change some of the moves' parameters to create a different game outcome.

import FocusGame as fg

# Initializing an instance of FocusGame
game = fg.FocusGame(('PlayerA', 'Red'), ('PlayerB', 'Green'))

# The first move of the game
print(game.move_piece('PlayerA', (0, 0), (0, 1), 1))  # Returns message "successfully moved"

# Testing out some of the status methods...
print(game.show_captured('PlayerA'))  # 0
print(game.show_reserve('PlayerA'))  # Returns 0
print(game.show_pieces((0, 1)))  # ['RED', 'RED']

# Demonstrating various built-in error messages
print(game.reserved_move('PlayerA', (0, 0)))  # Returns message "No pieces in reserve"
print(game.move_piece('PlayerA', (0, 1), (0, 2), 2))  # Returns "Not your turn"
print(game.move_piece('PlayerB', (0, 1), (0, 2), 1))  # Returns "Invalid location"
print(game.move_piece('PlayerB', (0, 2), (0, 4), 2))  # Returns "Invalid number of pieces"

# Back to regular gameplay
print(game.move_piece('PlayerB', (0, 2), (0, 3), 1))  # Returns "successfully moved"
print(game.move_piece('PlayerA', (0, 1), (0, 3), 2))  # Returns "successfully moved"
print(game.show_pieces((0, 3)))  # ['GREEN', 'GREEN', 'RED', 'RED']

# PlayerA's first capture!
print(game.move_piece("PlayerB", (4, 2), (4, 3), 1))
print(game.move_piece("PlayerA", (0, 3), (4, 3), 4))
print(game.show_captured("PlayerA"))  # 1
print(game.show_pieces((4, 3)))  # ['GREEN', 'GREEN', 'GREEN', 'RED', 'RED']

# PlayerA putting 2 pieces in reserve
print(game.move_piece("PlayerB", (1, 4), (1, 5), 1))
print(game.move_piece("PlayerA", (1, 2), (1, 3), 1))
print(game.move_piece("PlayerB", (1, 5), (1, 3), 2))
print(game.move_piece("PlayerA", (4, 3), (1, 3), 3))
print(game.show_pieces((1, 3)))  # ['GREEN', 'GREEN', 'GREEN', 'RED', 'RED']
print(game.show_reserve('PlayerA'))  # 2
print(game.show_captured("PlayerA"))  # 1

# PlayerA making a reserved move to capture another piece
print(game.move_piece("PlayerB", (5, 4), (5, 5), 1))
print(game.reserved_move('PlayerA', (1, 3)))
print(game.show_pieces((1, 3)))  # ['GREEN', 'GREEN', 'RED', 'RED', 'RED']
print(game.show_reserve('PlayerA'))  # 1
print(game.show_captured("PlayerA"))  # 2

# PlayerA making a reserved move to capture another piece
print(game.move_piece("PlayerB", (3, 4), (3, 5), 1))
print(game.reserved_move('PlayerA', (1, 3)))
print(game.show_pieces((1, 3)))  # ['GREEN', 'RED', 'RED', 'RED', 'RED']
print(game.show_reserve('PlayerA'))  # 0
print(game.show_captured("PlayerA"))  # 3

# PlayerB stacking up 5 of their pieces...
print(game.move_piece("PlayerB", (3, 5), (5, 5), 2))
print(game.move_piece("PlayerA", (4, 0), (4, 1), 1))
print(game.move_piece("PlayerB", (5, 5), (5, 1), 4))
print(game.show_pieces((5, 1)))  # ['GREEN', 'GREEN', 'GREEN', 'GREEN', 'GREEN']

# Player A is getting ready to make a big move...
print(game.move_piece("PlayerA", (5, 3), (5, 2), 1))
print(game.move_piece("PlayerB", (1, 0), (1, 1), 1))
print(game.move_piece("PlayerA", (1, 3), (1, 1), 2))
print(game.show_pieces((1, 1)))  # ['GREEN', 'GREEN', 'RED', 'RED']

#Player B doesn't see what's coming...
print(game.move_piece("PlayerB", (3, 0), (3, 1), 1))

# PlayerA's winning move!
print(game.move_piece("PlayerA", (1, 1), (5, 1), 4)) # PlayerA Wins
print(game.show_pieces((5, 1)))  # ['GREEN', 'GREEN', 'GREEN', 'RED', 'RED']
print(game.show_reserve('PlayerA'))  # 0
print(game.show_captured("PlayerA"))  # 7
