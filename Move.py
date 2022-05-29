import constants as _

class Move:
    def __init__(self, curr_square, target_square, board):
        self._curr_square = curr_square
        self._target_loc = target_square
        self._board = board

    def __str__(self):
        return str(self._curr_square[0]) + ',' + str(self._curr_square[1]) + ',' + \
               str(self._target_loc[0]) + ',' + str(self._target_loc[1]) + ' '

    def __eq__(self, other):
        if isinstance(other, Move):
            return self._curr_square == other._curr_square and self._target_loc == other._target_loc

        return False

    def is_capture_move(self):
        """
        Returns True if the move object is a capture one where both its column and
        row differential absolut values are equal to 2.
        """

        return True if abs(self._curr_square[0] - self._target_loc[0]) == \
                       abs(self._curr_square[1] - self._target_loc[1]) == 2 else False


    def is_regular_move(self):
        """
        Returns True if the move object is a regular one where both its column and
        row differential absolut values are equal to 1.
        """

        return True if abs(self._curr_square[0] - self._target_loc[0]) == \
                       abs(self._curr_square[1] - self._target_loc[1]) == 1 else False


    def move_to_validate(self):
        """
        Checking if the move object is legal or not. Returns True or False respectively.
        """

        if not (self.is_regular_move() or self.is_capture_move()):
            return False

        if not all((0 <= index < _.BOARD_SIZE) for index in (self._curr_square + self._target_loc)):
            return False

        if self._board.table[self._target_loc] != _.EMPTY:
            return False

        return True

    def get_move(self):
        """
        Returns move object current and target squares tuple.
        """

        return self._curr_square, self._target_loc

