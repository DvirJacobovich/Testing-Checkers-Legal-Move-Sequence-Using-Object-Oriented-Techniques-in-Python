import constants as _

class Board:
    def __init__(self):
        # initialing the board according to instructions in self.table.
        self.table = {(i, j): _.EMPTY for i in range(_.BOARD_SIZE) for j in range(_.BOARD_SIZE)}
        for i in range(_.BOARD_SIZE):
            for j in range(_.BOARD_SIZE):
                curr_loc = (j, i)
                if i < 3:
                    if (i == 0 or i == 2) and j % 2 != 0:
                        self.table[curr_loc] = _.WHITE_SYMBOL

                    elif i == 1 and j % 2 == 0:
                        self.table[curr_loc] = _.WHITE_SYMBOL

                if i >= 5:
                    if (i == 5 or i == 7) and j % 2 == 0:
                        self.table[curr_loc] = _.BLACK_SYMBOL
                    elif i == 6 and j % 2 != 0:
                        self.table[curr_loc] = _.BLACK_SYMBOL


    def display_board(self, turn):
        """
        Method that visualises the abstract board by printing self.table
        """

        print('Its' + turn + 'turn! \n')
        for i in range(_.BOARD_SIZE):
            for j in range(_.BOARD_SIZE):
                print(self.table[(i, j)], end='\t')

            print('\n')
        print('\n')

