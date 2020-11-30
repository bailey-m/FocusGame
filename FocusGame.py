#Name: Meredith Bailey
#Date: 11/29/2020
#Description: Contains classes and methods needed to play FocusGame.


class Player:
    """
    Represents a player of the FocusGame. Has name and color attributes, as well as attributes to count captured and
    reserved pieces. Has getter methods for all attributes, as well as methods to add/decrement reserved pieces and add
    captured pieces.
    Player objects are initialized when a FocusGame object is initialized. Initialization of a FocusGame object requires
    name and color piece parameters for two players, and these parameters are then used to initialize two Player objects.
    Player objects are stored in and used by FocusGame objects, so that the FocusGame object can utilize the Player's color,
    reserved, and captured attributes when doing game logic that checks for wins, makes reserve moves, puts pieces into
    reserve and capture, checks for correct color on top of the stack, etc.
    """
    def __init__(self, name, color):
        """
        Initializes a player of FocusGame. Takes in the player's name and color of piece they're playing.
        Initializes captured and reserve counts to 0.
        :param name: player's name (string)
        :param color: player's color (string)
        """
        self._name = name.upper()
        self._color = color.upper()
        self._captured = 0
        self._reserved = 0

    def get_color(self):
        """
        :return: player color (string).
        """
        return self._color

    def get_name(self):
        """
        :return: player name (string).
        """
        return self._name

    def get_captured_pieces(self):
        """
        :return: number of captured pieces (int)
        """
        return self._captured

    def get_reserved_pieces(self):
        """
        :return: number of reserved pieces (int)
        """
        return self._reserved

    def decrement_reserved_pieces(self):
        """
        Subtracts 1 from the number of reserved pieces.
        :return: None
        """
        self._reserved -= 1

    def add_reserved_piece(self):
        """
        Adds 1 to the number of reserved pieces.
        :return: None
        """
        self._reserved += 1

    def add_captured_piece(self):
        """
        Adds 1 to the number of captured pieces.
        :return: None
        """
        self._captured += 1


class Space:
    """
    Represents a space on the FocusGame board. Multiple pieces on the space are represented by a list (the stack attribute),
    with lowest piece at index 0, and top piece at highest index.
    Has methods for adding a piece, removing pieces from top and bottom, getting length, and getting the stack itself.
    Space objects are initialized in a 6x6 list of lists (to represent the board) when a FocusGame object is initialized.
    """
    #
    def __init__(self, starting_piece):
        """Initializes a Space object. If given a starting piece, adds that starting piece to the stack.
        :param starting_piece: the color of the piece on the space at the start of the game. (string)"""
        if not starting_piece:
            self._stack = []
        else:
            self._stack = [starting_piece.upper()]

    def add_piece(self, piece):
        """
        Adds piece to top of the stack (end of the stack list).
        :param piece: the color of the piece to add (string)
        :return: None
        """
        self._stack.append(piece)

    def pop_top(self):
        """
        Removes the piece on the top of the stack (at the end of the stack list) and returns it.
        :return: piece (string)
        """
        if not self.is_empty():
            return self._stack.pop(len(self._stack) - 1)
        return None

    def get_top(self):
        """
        Returns the piece on the top of the stack without removing it.
        Used for checking the color of the piece on the top of the stack.
        :return: piece (string)
        """
        if not self.is_empty():
            return self._stack[len(self._stack) - 1]
        return None

    def is_empty(self):
        """
        Checks if the stack is empty.
        Used to prevent errors in other Space methods.
        :return: boolean
        """
        if len(self._stack) == 0:
            return True
        return False

    def remove_pieces_from_bottom(self):
        """
        If the stack has over 5 pieces in it, removes pieces from the bottom of the stack (beginning of the stack list)
        until the stack has only 5 pieces in it. Returns a list of all pieces removed and stores it in extra_pieces.
        Used when capturing and reserving pieces after a move has been made.
        :return: extra_pieces (list of pieces removed)
        """
        extra_pieces = []
        if len(self._stack) > 5:
            extra_qty = len(self._stack) - 5
            for i in range(extra_qty):
                extra_pieces.append(self._stack.pop(0))
        return extra_pieces

    def remove_pieces_from_top(self, num_pieces):
        """
        Removes a specified number of pieces from the top of the stack, and returns them in a list.
        Used when making a single or multiple move.
        Returns a list of pieces in reverse order of how they'll be placed on the destination space,
        i.e. the top piece of the stack of moving pieces is at index 0 in piece_stack.
        :param num_pieces: number of pieces to remove from top (int)
        :return: piece_stack (list of pieces removed)
        """
        piece_stack = []
        for i in range(num_pieces):
            piece_stack.append(self.pop_top())
        return piece_stack

    def get_length(self):
        """
        :return: length of stack / number of pieces on the space. (int)
        """
        return len(self._stack)

    def get_stack(self):
        """
        :return: list of pieces in the stack. (list)
        """
        return self._stack


class FocusGame:
    """
    Represents the Focus game. Has attributes for two players, each of which are a Player object. Has an attribute to
    track whose turn it is, and a "board" attribute that uses a list of lists (of Space objects) to represent the board.
    The main methods used for gameplay are the move_piece and reserved_move methods. The make_move, change_turn, and
    reserve_and_capture methods perform subtasks for the main gameplay methods. is_win and check_reserve_and_capture check
    for winning condition and reserve/capture condition, respectively.
    The find_player_by_name method is used to identify the Player object making the current move, and the get_space
    method is used to identify the Space objects at the move's origin/destination.
    Several methods validate user input for the main gameplay methods, such as is_correct_turn, is_valid_position,
    is_valid_location, and is_valid_piece_num.
    Additionally, there are methods to show current statuses within the game, such as show_pieces, show_reserve, and show_captured.
    """

    def __init__(self, player_a, player_b):
        """
        Initializes a Focus Game. Takes in names and playing piece colors of two players and initializes Player objects.
        Player names cannot be identical, and are not case-sensitive.
        Initializes a 6x6 board (as a list of lists) of Space objects, which are each initialized with a Player object's color
        as its first piece in that Space's stack.
        Initializes the current_turn attribute to None, so that either player can go first. After the first turn, the
        current_turn attribute will be set to a Player object and checked for equality with the current Player object at
        the start of each turn.
        :param player_a: tuple containing: (player A name, player A color)
        :param player_b: tuple containing: (player B name, player A color)
        """
        self._player_a = Player(player_a[0].upper(), player_a[1].upper())
        self._player_b = Player(player_b[0].upper(), player_b[1].upper())
        self._current_turn = None  # will be Player object
        self._board = [[Space(self._player_a.get_color()), Space(self._player_a.get_color()), Space(self._player_b.get_color()), Space(self._player_b.get_color()), Space(self._player_a.get_color()), Space(self._player_a.get_color())],
                      [Space(self._player_b.get_color()), Space(self._player_b.get_color()), Space(self._player_a.get_color()), Space(self._player_a.get_color()), Space(self._player_b.get_color()), Space(self._player_b.get_color())],
                      [Space(self._player_a.get_color()), Space(self._player_a.get_color()), Space(self._player_b.get_color()), Space(self._player_b.get_color()), Space(self._player_a.get_color()), Space(self._player_a.get_color())],
                      [Space(self._player_b.get_color()), Space(self._player_b.get_color()), Space(self._player_a.get_color()), Space(self._player_a.get_color()), Space(self._player_b.get_color()), Space(self._player_b.get_color())],
                      [Space(self._player_a.get_color()), Space(self._player_a.get_color()), Space(self._player_b.get_color()), Space(self._player_b.get_color()), Space(self._player_a.get_color()), Space(self._player_a.get_color())],
                      [Space(self._player_b.get_color()), Space(self._player_b.get_color()), Space(self._player_a.get_color()), Space(self._player_a.get_color()), Space(self._player_b.get_color()), Space(self._player_b.get_color())]]

    def move_piece(self, player_name, orig_coord, dest_coord, num_pieces):
        """
        Calls methods to check for correct player turn, valid origin and destination locations, and valid number of pieces.
        If everything is valid, calls methods to make the pieces move from origin to destination, check for need to
        reserve and capture, check for a win, and change current turn.
        :param player_name: name of player taking turn (string)
        :param orig_coord: coordinates of origin space, where pieces are moving from (tuple: (row, col))
        :param dest_coord: coordinates of destination space, where pieces are moving to (tuple: (row, col))
        :param num_pieces: number of pieces to move from origin space
        :return: status message (string)
        """
        player = self.find_player_by_name(player_name)
        if not self.is_correct_turn(player):
            return "Not your turn"

        if not self.is_valid_location(player, orig_coord, dest_coord, num_pieces):
            return "Invalid location"

        orig = self.get_space(orig_coord)
        if not self.is_valid_piece_num(orig, num_pieces):
            return "Invalid number of pieces"

        dest = self.get_space(dest_coord)
        self.make_move(orig, dest, num_pieces)
        self.check_reserve_and_capture(dest, player)

        if self.is_win(player):
            return player_name + " Wins"

        self.change_turn(player)
        return "Successfully moved"

    def show_pieces(self, position):
        """
        Shows the stack of pieces at a given space in form of a list, with bottom-most piece at index 0.
        :param position: coordinates of space (tuple: (row, col))
        :return: stack (list)
        """
        if not self.is_valid_position(position):
            return None
        return self._board[position[0]][position[1]].get_stack()

    def show_reserve(self, player_name):
        """
        Shows count of reserved pieces for a given player.
        :param player_name: name of player (string)
        :return: count of reserved pieces (int)
        """
        player = self.find_player_by_name(player_name)
        if player:
            return player.get_reserved_pieces()
        return

    def show_captured(self, player_name):
        """
        Shows count of captured pieces for a given player.
        :param player_name: name of player (string)
        :return: count of captured pieces (int)
        """
        player = self.find_player_by_name(player_name)
        if player:
            return player.get_captured_pieces()
        return

    def reserved_move(self, player_name, position):
        """
        Calls method to validate destination of reserve piece and validate that the player has pieces in reserve.
        If destination and reserve pieces are valid, calls methods to add piece to destination stack, decrease
        player's reserved pieces by 1, check for reserve and capture at destination, check for a win, and change turns.
        :param player_name: name of player making move (string)
        :param position: destination of reserve piece (tuple: (row, col))
        :return: status message (string)
        """
        # check if valid position
        if not self.is_valid_position(position):
            return

        # check if player has pieces in reserve
        player = self.find_player_by_name(player_name)
        if not player or player.get_reserved_pieces() == 0:
            return "No pieces in reserve"

        # add a reserved piece onto the destination stack, and subtract one from player's reserved pieces
        dest = self.get_space(position)
        dest.add_piece(player.get_color())
        player.decrement_reserved_pieces()

        # check for reserve and capture, check for win condition, change turn
        self.check_reserve_and_capture(dest, player)
        if self.is_win(player):
            return player_name + " Wins"
        self.change_turn(player)

    def is_valid_position(self, position):
        """
        Checks the the coordinates in the position are valid coordinates.
        :param position: coordinates of space (tuple: (row, col))
        :return: boolean
        """
        if position[0] < 0 or position[1] < 0 or position[1] > 5 or position[1] > 5:
            return False
        return True

    def get_space(self, position):
        """
        Takes in the coordinates of a space and returns the Space object at those coordinates.
        Assumes valid space - must be used after is_valid_position is used to validate position.
        :param position: coordinates of space (tuple: (row, col))
        :return: Space object
        """
        return self._board[position[0]][position[1]]

    def find_player_by_name(self, name):
        """
        Takes in a player's name and returns the Player object with that name.
        :param name: player's name (string)
        :return: Player object
        """
        if name.upper() == self._player_a.get_name():
            return self._player_a
        elif name.upper() == self._player_b.get_name():
            return self._player_b
        return None

    def change_turn(self, current_player):
        """
        Sets the current_turn attribute, based on who is the current player.
        :param current_player: current player taking turn (Player object)
        :return: None
        """
        if current_player == self._player_a:
            self._current_turn = self._player_b
        else:
            self._current_turn = self._player_a

    def check_reserve_and_capture(self, dest, player):
        """
        Checks the stack at a given destination for if it has more than 5 pieces.
        If it does, calls a method to reserve and capture pieces.
        :param dest: destination space on board (Space object)
        :param player: current player making move (Player object)
        :return: None
        """
        if dest.get_length() > 5:
            self.reserve_and_capture_pieces(dest, player)

    def reserve_and_capture_pieces(self, dest, player):
        """
        Calls method to remove pieces from the bottom of the stack at a given space, until the stack has only 5 pieces left.
        Then, adds to either the current player's reserved or captured count, based on the colors of the pieces removed.
        :param dest: destination space on board (Space object)
        :param player: current player making move (Player object)
        :return: None
        """
        extra_pieces = dest.remove_pieces_from_bottom()
        for piece in extra_pieces:
            if piece == player.get_color():
                player.add_reserved_piece()
            else:
                player.add_captured_piece()

    def is_win(self, player):
        """
        Checks for winning condition by checking how many captured pieces the current player has.
        If current player's captured pieces are at least 6, the player wins.
        :param player: current player taking turn (Player object)
        :return: boolean
        """
        if player.get_captured_pieces() >= 6:
            return True
        return False

    def make_move(self, orig, dest, num_pieces):
        """Removes pieces from the origin space, and adds them to the destination space.
        Calls a method to remove pieces from the origin space, which are stored in a list named pieces_moved.
        The pieces in pieces_moved are listed in reverse order, i.e. the top piece, which should be added to the
        destination stack last, is at index 0. Therefore, this method adds pieces to the destination stack starting
        with the last piece in pieces_moved, and moving toward the front of the list.
        :param orig: the origin space (Space object)
        :param dest: the destination space (Space object)
        :param num_pieces: the number of pieces being moved
        """
        pieces_moved = orig.remove_pieces_from_top(num_pieces)
        for i in range(len(pieces_moved)):
            dest.add_piece(pieces_moved[len(pieces_moved) - 1 - i])

    def is_correct_turn(self, player):
        """
        Checks if it is a given player's turn.
        :param player: player currently making move (Player object)
        :return: boolean
        """
        if self._current_turn is not None and player != self._current_turn:
            return False
        return True

    def is_valid_location(self, player, orig_coord, dest_coord, num_pieces):
        """
        Checks if valid locations were given by player when they were attempting to make a move.
        :param player: player currently making move (Player object)
        :param orig_coord: coordinates of origin space, where pieces are moving from (tuple: (row, col))
        :param dest_coord: coordinates of destination space, where pieces are moving to (tuple: (row, col))
        :param num_pieces: number of pieces being moved (int)
        :return: boolean
        """
        # if invalid origin or destination coordinates
        if not self.is_valid_position(orig_coord) or not self.is_valid_position(dest_coord):
            return False

        # if orig is a stack with their piece not on top
        orig = self.get_space(orig_coord)
        if orig.get_top() != player.get_color():
            return False

        # invalid location if attempt to move diagonally
        row_diff = dest_coord[0] - orig_coord[0]
        col_diff = dest_coord[1] - orig_coord[1]
        if row_diff != 0 and col_diff != 0:
            return False

        # invalid location if spaces moved is not equal to number of pieces being moved
        if row_diff == 0:
            spaces_moved = abs(col_diff)
        else:
            spaces_moved = abs(row_diff)
        if num_pieces != spaces_moved:
            return False

        return True

    def is_valid_piece_num(self, orig, num_pieces):
        """
        Checks if a valid number of pieces are being moved by player when they are attempting to make a move.
        :param orig: origin space (Space object)
        :param num_pieces: number of pieces being moved (int)
        :return: boolean
        """
        if num_pieces > orig.get_length():
            return False
        return True
