import Board
import constants as _
import Move as m


class Checkers:
    @staticmethod
    def get_natural_diagonal(natural_move, square):
        return tuple([sum(x) for x in zip(natural_move, square)])

    @staticmethod
    def coordinates_validate(square):
        return False if not all((0 <= index < _.BOARD_SIZE) for index in square) else True

    @staticmethod
    def get_captured_loc(square, target_square):
        return abs(square[0] + target_square[0]) / 2, abs(square[1] + target_square[1]) / 2


    def __init__(self, moves):
        self._board = Board.Board()
        self._player_symbol, self.__opponent_symbol = _.WHITE_SYMBOL, _.BLACK_SYMBOL
        self._player_natural_directions = _.WHITE_NATURAL_DIRECTIONS
        self._player, self._opponent = _.WHITE, _.BLACK  # (=1 for white, =0 black)
        self._whites_counter = self._blacks_counter = _.INITIAL_NUM_PIECES
        self._game_moves = [m.Move(moves[i][0], moves[i][1], self._board) for i in range(len(moves))]
        self._total_game_moves = len(self._game_moves)
        self._current_line = 0
        self._illegal_move = self._game_moves[0]
        self._is_illegal_move = False
        self._game_on = True


    def game_runner(self):
        """
        Method that runs the game. Responsible for making players' moves by calling
        self.make_move method, switching turns, testing the program ending criterion
        every round and setting the winner if there is any.
        """

        while self._game_on:
            curr_move = self._game_moves[self._current_line]
            self.make_player_move(curr_move)
            self.switch_players()

            # checking program ending criterion: illegal move.
            if self._is_illegal_move:
                print(_.ILLEGAL_MESSAGE_ONE, self._current_line + 1, _.ILLEGAL_MESSAGE_TWO, self._illegal_move)
                self._game_on = False

            # checking program ending criterion: no legal move to perform (also game ends).
            elif not self.get_all_valid_moves():
                if self._whites_counter > self._blacks_counter:
                    print(_.WHITE_VICTORY)

                elif self._blacks_counter > self._whites_counter:
                    print(_.BLACK_VICTORY)

                else:
                    print(_.TIE_GAME)

                self._game_on = False

            # checking program ending criterion: reached the final move.
            elif self._current_line == self._total_game_moves:
                print(_.INCOMPLETE_GAME)
                self._game_on = False


    def is_empty_square(self, square):
        """
        Returns True if the square is empty. False otherwise.
        """

        return True if self._board.table[square] == _.EMPTY else False


    def get_player_all_pieces(self):
        """
        Returns player all pieces locations in a list of tuples.
        """

        return list(dict(filter(lambda piece: piece[1] == self._player_symbol,
                                self._board.table.items())).keys())


    def switch_players(self):
        """
        Switch between the two players by switching the self.player also
        the self.player_symbol, and the self.player_natural_directions.
        """

        self._player = 1 - self._player  # switch turns
        if self._player:
            self._player_symbol = _.WHITE_SYMBOL
            self.__opponent_symbol = _.BLACK_SYMBOL
            self._player_natural_directions = _.WHITE_NATURAL_DIRECTIONS

        else:
            self._player_symbol = _.BLACK_SYMBOL
            self.__opponent_symbol = _.WHITE_SYMBOL
            self._player_natural_directions = _.BLACK_NATURAL_DIRECTIONS


    def regular_move(self, curr_square, new_square):
        """
        Method that performs the regular move on the Board object by setting
        the current player symbol at the new_square and empty the its old square.
        """

        self._board.table[curr_square] = _.EMPTY
        self._board.table[new_square] = self._player_symbol


    def capture_move(self, curr_square, captured_square, new_square):
        """
        Method that performs the capture move on the Board object by setting
        the capture and captured locations to empty and the target one to the
        current player symbol.
        """

        self._board.table[curr_square] = _.EMPTY
        self._board.table[captured_square] = _.EMPTY
        self._board.table[new_square] = self._player_symbol
        if self._player:
            self._blacks_counter -= 1

        else:
            self._whites_counter -= 1


    def make_player_move(self, curr_move):
        """
        Method that performs the current player move according to the given moves input pointer.
        """

        if curr_move.move_to_validate():
            curr_square, target_square = curr_move.get_move()
            if curr_move.is_capture_move():
                row, col = self.get_captured_loc(curr_square, target_square)
                self.capture_move(curr_square, (row, col), target_square)
                self._current_line += 1

                # checking sequential capture options.
                potential_sequential_captures = self.potential_capture(target_square)
                while potential_sequential_captures and self._current_line < self._total_game_moves:
                    next_move = self._game_moves[self._current_line]
                    if next_move in potential_sequential_captures:
                        curr_square, target_square = next_move.get_move()
                        row, col = self.get_captured_loc(curr_square, target_square)
                        self.capture_move(curr_square, (row, col), target_square)
                        potential_sequential_captures = self.potential_capture(target_square)
                        self._current_line += 1
                        continue

                    self._is_illegal_move = True
                    self._illegal_move = self._game_moves[self._current_line]
                    return

            elif curr_move.is_regular_move():
                all_pieces = self.get_player_all_pieces()
                for piece_loc in all_pieces:
                    if self.potential_capture(piece_loc):
                        # the move is regular while there are potential capture moves.
                        self._is_illegal_move = True
                        self._illegal_move = self._game_moves[self._current_line]
                        return

                self.regular_move(curr_square, target_square)
                self._current_line += 1

        else:
            self._is_illegal_move = True
            self._illegal_move = self._game_moves[self._current_line]

    def potential_capture(self, square):
        """
        Method that checks if there is any potential captures for the current player for
        specific player piece location, and return list with all capture moves objects.
        """

        potential_captures = list()
        for direction in self._player_natural_directions:
            captured_square = self.get_natural_diagonal(direction, square)
            if self.coordinates_validate(captured_square) and\
                    self._board.table[captured_square] == self.__opponent_symbol:
                target_square = self.get_natural_diagonal(direction, captured_square)
                if self.coordinates_validate(target_square) and self.is_empty_square(target_square):
                    potential_captures.append(m.Move(square, target_square, self._board))

        return potential_captures



    def get_all_valid_moves(self):
        """
        Returns list of all legal moves objects. Since when there is a potential capture
        move all regulars are illegal, thus the legal moves can be one of two options:
        1. all regular moves.
        2. all capture moves.

        """

        all_pieces = self.get_player_all_pieces()
        all_valid_moves = list()
        for piece_square in all_pieces:
            potential_captures = self.potential_capture(piece_square)
            if potential_captures:
                all_valid_moves.extend(self.potential_capture(piece_square))

        if not all_valid_moves:
            for piece_square in all_pieces:
                for direction in self._player_natural_directions:
                    potential_diagonal = self.get_natural_diagonal(direction, piece_square)
                    move = m.Move(piece_square, potential_diagonal, self._board)
                    if move.move_to_validate() and move.is_regular_move():
                        all_valid_moves.append(move)

        return all_valid_moves

