# MTELFR = mask_to_extract_last_filled_row
# MTECS = mask_to_extract_column_state
# MTECWLF = mask_to_extract_state_with_lastfilledcolumn
# assume column start with 1
# assume binary representation starts from right
# each column is represented by 9 bits 3 for last filled row in the column 6 for the plays in the column
# the 3 bits of the last filled row in the column also are at the right of the 9 bits
# the 6 bits of the play the first play (row 1) is the first bit from the right
# computer is 0 & human is 1
import numpy as np


def get_score(f1, f2, f3, f4, player):
    four = 0
    three = 0
    two = 0
    if f1 == player and f2 == player and f3 == player and f4 == player:
        four += 1
    elif f1 == '*' and f2 == player and f3 == player and f4 == player:
        three += 1
    elif f1 == player and f2 == '*' and f3 == player and f4 == player:
        three += 1
    elif f1 == player and f2 == player and f3 == '*' and f4 == player:
        three += 1
    elif f1 == player and f2 == player and f3 == player and f4 == '*':
        three += 1
    elif f1 == player and f2 == player and f3 == '*' and f4 == '*':
        two += 1
    elif f1 == '*' and f2 == '*' and f3 == player and f4 == player:
        two += 1
    elif f1 == player and f2 == '*' and f3 == '*' and f4 == player:
        two += 1
    elif f1 == '*' and f2 == player and f3 == player and f4 == '*':
        two += 1
    elif f1 == '*' and f2 == player and f3 == '*' and f4 == player:
        two += 1
    elif f1 == player and f2 == '*' and f3 == player and f4 == '*':
        two += 1

    return four, three, two


class State:
    computer = 0
    human = 1

    def __init__(self, state):
        self.state = state
        self.computer_score = 0
        self.human_score = 0
        self.col_num = -1
        self.neighbours = []

    def get_neighbours(self, player_num):
        neighbours = []
        for i in range(1, 8):
            if self.valid_play(i):
                new_state = self.update_state(i, player_num)
                new_state.col_num = i
                neighbours.append(new_state)

        return neighbours

    def valid_play(self, col_num):
        MTELFR = 7
        MTELFR = MTELFR << ((col_num - 1) * 9)
        LastFilledRow = self.state & MTELFR
        LastFilledRow = LastFilledRow >> ((col_num - 1) * 9)
        return LastFilledRow < 6

    def print_state(self):

        board = self.get_board()

        print(np.matrix(board))

    # updated -> if last filled row = 6 return the same state
    def update_state(self, col_num, playerNum):
        temp_state = State(self.state)
        MTELFR = 7  # MTELFR = mask_to_extract_last_filled_row
        MTECS = 63  # MTECS = mask_to_extract_column_state
        play = 1

        MTELFR = MTELFR << ((col_num - 1) * 9)
        LastFilledRow = temp_state.state & MTELFR
        LastFilledRow = LastFilledRow >> ((col_num - 1) * 9)

        if LastFilledRow == 6:
            print("This column is already filled")
            return temp_state

        MTECS = MTECS << ((col_num - 1) * 9 + 3)
        colState = temp_state.state & MTECS
        colState = colState >> ((col_num - 1) * 9 + 3)

        play = play << LastFilledRow
        play = ~play if playerNum == 0 else play

        if playerNum == 0:
            colState = colState & play
        else:
            colState = colState | play

        LastFilledRow += 1

        remainder = temp_state.state >> (col_num * 9)
        remainder = remainder << (col_num * 9)

        temp_state.state = temp_state.state | MTELFR
        temp_state.state = ~ temp_state.state
        LastFilledRow = ~ LastFilledRow
        LastFilledRow = LastFilledRow << ((col_num - 1) * 9)
        # LastFilledRow = LastFilledRow << (54-(col_num*9))
        # LastFilledRow = LastFilledRow >> (54-(col_num*9))
        temp_state.state = temp_state.state | LastFilledRow
        temp_state.state = ~ temp_state.state
        # self.state = self.state & LastFilledRow

        temp_state.state = temp_state.state | MTECS
        temp_state.state = ~ temp_state.state
        colState = ~ colState
        colState = colState << ((col_num - 1) * 9 + 3)
        # colState = colState << (54-(col_num*9) + 3)
        # colState = colState >> (54-(col_num*9) + 3)
        temp_state.state = temp_state.state | colState
        temp_state.state = ~ temp_state.state
        # self.state = self.state & colState

        temp_state.state = temp_state.state | remainder
        # temp_state.parent = self

        return temp_state

    def get_total_score(self):
        score_human,_,_ = self.calculate_heuristic(State.human)
        score_computer,_,_ = self.calculate_heuristic(State.computer)

        return score_human, score_computer

    def get_pointsSideRow2(self, col_num, LastFilledRow, player_num):
        points_from_sideRow2 = 0
        counter = 0
        if (7 - col_num + 1) <= LastFilledRow:
            start = 7
            play_to_get = LastFilledRow - (7 - col_num + 1) + 1
        else:
            start = (7 - col_num + 1) - LastFilledRow + 1
            start = 7 - start + 1
            play_to_get = 1

        sideRow2row = play_to_get
        sideRow2col = start
        sideRow2rowAllowed = True

        for i in range(start, 0, -1):
            if start - 0 < 4:
                sideRow2rowAllowed = False
                break
            LastFilledCRow, cState = self.get_last_col_and_state(i)

            if LastFilledCRow < play_to_get:
                counter = 0
                continue

            c = self.get_play(cState, play_to_get)
            play_to_get += 1
            if c == player_num:
                counter += 1
            else:
                counter = 0

            if counter == 4:
                points_from_sideRow2 += 1
                counter -= 1

            if play_to_get > 6:
                break

        return points_from_sideRow2, sideRow2row, sideRow2col, sideRow2rowAllowed

    def get_pointsSideRow1(self, col_num, LastFilledRow, player_num):
        points_from_sideRow1 = 0
        counter = 0
        if col_num <= LastFilledRow:
            start = 1
            play_to_get = LastFilledRow - col_num + 1
        else:
            start = col_num - LastFilledRow + 1
            play_to_get = 1

        sideRow1row = play_to_get
        sideRow1col = start
        sideRow1rowAllowed = True

        for i in range(start, 8):
            if 8 - start < 4:
                sideRow1rowAllowed = False
                break
            LastFilledCRow, cState = self.get_last_col_and_state(i)

            if LastFilledCRow < play_to_get:
                counter = 0
                continue

            c = self.get_play(cState, play_to_get)
            play_to_get += 1
            if c == player_num:
                counter += 1
            else:
                counter = 0

            if counter == 4:
                points_from_sideRow1 += 1
                counter -= 1

            if play_to_get > 6:
                break

        return points_from_sideRow1, sideRow1row, sideRow1col, sideRow1rowAllowed

    def get_pointsColumn(self, player_num, LastFilledRow, colState):
        pointMask = 15
        points_from_column = 0
        if not player_num: colState = ~ colState
        for i in range(LastFilledRow - 3):  # max iterations is 3
            temp = pointMask & colState
            if temp == pointMask:
                points_from_column += 1
            pointMask = pointMask << 1

        return points_from_column

    def get_pointsRow(self, player_num, LastFilledRow):
        points_from_row = 0
        counter = 0
        for i in range(1, 8):
            LastFilledCRow, cState = self.get_last_col_and_state(i)
            if LastFilledCRow < LastFilledRow:
                counter = 0
                continue

            c = self.get_play(cState, LastFilledRow)
            if c == player_num:
                counter += 1
            else:
                counter = 0

            if counter == 4:
                points_from_row += 1
                counter -= 1

        return points_from_row

    # this is called after the new state is updated
    def get_new_score(self, col_num, player_num):  # , score_analysis):
        print("iam here")
        # ????????????????????????????????
        if self.parent is None:
            score = 0
        else:
            if player_num == State.computer:
                score = self.parent.computer_score
            else:
                score = self.parent.human_score

        if player_num == State.computer:
            score_analysis = self.computer_score_analysis
        else:
            score_analysis = self.human_score_analysis

        # ????????????????????????????????

        LastFilledRow, colState = self.get_last_col_and_state(col_num)
        print("Last filled row is " + str(LastFilledRow))

        points_from_column = self.get_pointsColumn(player_num, LastFilledRow, colState)
        points_from_row = self.get_pointsRow(player_num, LastFilledRow)
        points_from_sideRow1, sideRow1row, sideRow1col, sideRow1rowAllowed = self.get_pointsSideRow1(col_num,
                                                                                                     LastFilledRow,
                                                                                                     player_num)
        points_from_sideRow2, sideRow2row, sideRow2col, sideRow2rowAllowed = self.get_pointsSideRow2(col_num,
                                                                                                     LastFilledRow,
                                                                                                     player_num)

        # print(points_from_row)
        # print(points_from_column)
        # print(points_from_sideRow1)
        # print(points_from_sideRow2)

        points_from_row -= score_analysis['r' + str(LastFilledRow)]
        points_from_column -= score_analysis['c' + str(col_num)]
        if sideRow1row < 4 and sideRow1rowAllowed:
            points_from_sideRow1 -= score_analysis['rc' + str(sideRow1row) + str(sideRow1col)]
        if sideRow2row < 4 and sideRow2rowAllowed:
            points_from_sideRow2 -= score_analysis['rc' + str(sideRow2row) + str(sideRow2col)]

        score += points_from_row + points_from_column + points_from_sideRow2 + points_from_sideRow1

        score_analysis['r' + str(LastFilledRow)] += points_from_row
        score_analysis['c' + str(col_num)] += points_from_column
        if sideRow1row < 4 and sideRow1rowAllowed:
            score_analysis['rc' + str(sideRow1row) + str(sideRow1col)] += points_from_sideRow1
        if sideRow2row < 4 and sideRow2rowAllowed:
            score_analysis['rc' + str(sideRow2row) + str(sideRow2col)] += points_from_sideRow2

        if player_num == State.computer:
            self.computer_score_analysis = score_analysis
            # print(self.computer_score_analysis)
        else:
            self.human_score_analysis = score_analysis
            # print(self.human_score_analysis)

        return score

    def get_last_col_and_state(self, col_num):
        MTELFR = 7  # MTELFR = mask_to_extract_last_filled_row
        MTECS = 63  # MTECS = mask_to_extract_column_state

        MTELFR = MTELFR << ((col_num - 1) * 9)
        LastFilledRow = self.state & MTELFR
        LastFilledRow = LastFilledRow >> ((col_num - 1) * 9)

        MTECS = MTECS << ((col_num - 1) * 9 + 3)
        colState = self.state & MTECS
        colState = colState >> ((col_num - 1) * 9 + 3)

        return LastFilledRow, colState

    def get_play(self, cState, LastFilledRow):
        MTELFR = 1  # MTELFR = mask_to_extract_last_filled_row

        MTELFR = MTELFR << (LastFilledRow - 1)
        c = cState & MTELFR
        c = c >> (LastFilledRow - 1)

        return c

    def get_board(self):
        temp_state = self.state
        listoflists = []
        for i in range(1, 8):
            alist = []
            MTELFR = 7  # MTELFR = mask_to_extract_last_filled_row
            MTECS = 63  # MTECS =  mask_to_extract_column_state
            MTELFR = MTELFR << ((i - 1) * 9)
            LastFilledRow = temp_state & MTELFR
            LastFilledRow = LastFilledRow >> ((i - 1) * 9)
            MTECS = MTECS << ((i - 1) * 9 + 3)
            colState = temp_state & MTECS
            colState = colState >> ((i - 1) * 9 + 3)

            for j in range(LastFilledRow):
                bit = colState & 1
                colState >>= 1
                alist.append(bit)

            for j in range(LastFilledRow, 6):
                alist.append("*")

            listoflists.append(alist)

        board = []
        for j in range(5, -1, -1):
            row = []
            for i in range(6, -1, -1):
                row.append(listoflists[i][j])
            board.append(row)
        return board

    def get_heuristic(self):
        fourC, threeC, twoC = self.calculate_heuristic(State.computer)
        fourH, threeH, twoH = self.calculate_heuristic(State.human)

        return (fourC*1000 + threeC*500 + twoC*200) - (fourH*1000 + threeH*500 + twoH*200)

    def calculate_heuristic(self, player, debug=False):

        board = self.get_board()
        four = 0
        three = 0
        two = 0
        for i in range(0, 6, 1):
            for j in range(0, 7, 1):
                if j + 3 < 7:
                    f1 = board[i][j]
                    f2 = board[i][j + 1]
                    f3 = board[i][j + 2]
                    f4 = board[i][j + 3]
                    current_four, current_three, current_two = get_score(f1, f2, f3, f4, player)
                    four += current_four
                    three += current_three
                    two += current_two

        for j in range(0, 7, 1):
            for i in range(0, 6, 1):
                if i + 3 < 6:
                    f1 = board[i][j]
                    f2 = board[i + 1][j]
                    f3 = board[i + 2][j]
                    f4 = board[i + 3][j]
                    current_four, current_three, current_two = get_score(f1, f2, f3, f4, player)
                    four += current_four
                    three += current_three
                    two += current_two

        for line in range(1, (6 + 7)):
            start_col = max(0, line - 6)
            count = min(line, (7 - start_col), 6)
            for j in range(0, count):
                if (min(6, line) - j - 3 - 1) >= 0 and (start_col + j + 3) < 7:
                    if debug:
                        print(min(6, line) - j - 1, start_col + j, sep="  ")
                    f1 = board[min(6, line) - j - 1][start_col + j]
                    f2 = board[min(6, line) - j - 1 - 1][start_col + j + 1]
                    f3 = board[min(6, line) - j - 2 - 1][start_col + j + 2]
                    f4 = board[min(6, line) - j - 3 - 1][start_col + j + 3]
                    current_four, current_three, current_two = get_score(f1, f2, f3, f4, player)
                    four += current_four
                    three += current_three
                    two += current_two

        for line in range((6 + 7) - 1, 0, - 1):
            start_col = min(6, line - 1)
            count = min((6 + 7) - line, start_col + 1, 6)
            for j in range(0, count):
                # print(min(6, (6 + 7) - line) - j - 1,start_col - j, sep="  ")
                if (min(6, (6 + 7) - line) - j - 3 - 1) >= 0 and (start_col - j - 3) > -1:
                    f1 = board[min(6, (6 + 7) - line) - j - 1][start_col - j]
                    f2 = board[min(6, (6 + 7) - line) - j - 1 - 1][start_col - j - 1]
                    f3 = board[min(6, (6 + 7) - line) - j - 2 - 1][start_col - j - 2]
                    f4 = board[min(6, (6 + 7) - line) - j - 3 - 1][start_col - j - 3]
                    current_four, current_three, current_two = get_score(f1, f2, f3, f4, player)
                    four += current_four
                    three += current_three
                    two += current_two
            # print()
        #
        if debug:
            print(four, three, two, sep='  ')
        return four , three , two

    def is_terminal(self):
        temp_state = self.state
        counter = 0
        for i in range(1, 8):
            MTELFR = 7  # MTELFR = mask_to_extract_last_filled_row
            MTELFR = MTELFR << ((i - 1) * 9)
            LastFilledRow = temp_state & MTELFR
            LastFilledRow = LastFilledRow >> ((i - 1) * 9)
            if LastFilledRow == 7:
                counter += 1

        return counter == 7

    def get_valid_col(self):
        for i in range(1, 8):
            if self.valid_play(i):
                return i


if __name__ == "__main__":
    s = State(68730783870)
    s = s.update_state(4, State.computer)
    s = s.update_state(4, State.computer)
    s = s.update_state(5, State.computer)
    s = s.update_state(6, State.computer)
    s = s.update_state(7, State.computer)
    s = s.update_state(5, State.computer)
    s = s.update_state(5, State.human)
    s = s.update_state(5, State.human)
    s = s.update_state(5, State.human)
    s = s.update_state(7, State.human)
    s = s.update_state(7, State.human)
    s = s.update_state(7, State.human)
    s = s.update_state(3, State.human)
    s.print_state()
    #print("current score ",s.get_total_score()[0], s.get_total_score()[1])
    s.calculate_heuristic(0, True)
