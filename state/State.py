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


class State:
    computer = 0
    human = 1

    def __init__(self, state):
        self.parent = None
        self.state = state
        self.computer_score = 0
        self.human_score = 0
        self.before = False
        self.heuristic_analysis_human = {
            "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }
        self.heuristic_analysis_computer = {
            "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }
        self.human_score_analysis = {
            "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }

        self.computer_score_analysis = {
            "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }
        '''
        self.score_analysis = {
            "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }
        '''
        self.heuristic_score_computer = 0
        self.heuristic_score_human = 0
        self.col_num = -1

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

    def try_heuristic(self):

        board = self.get_board()
        # self.print_state()
        comp_row_score = 0
        hum_row_score = 0

        for i in range(0, 6, 1):
            row = 1
            lis_row = []
            for j in range(1, 7, 1):
                if board[i][j] == board[i][j - 1]:
                    row += 1
                if (board[i][j] != board[i][j - 1]) or (
                        j == 6 and (board[i][j] == board[i][j - 1])):
                    prev = board[i][j - 1]
                    current = board[i][j]

                    x = (prev, row)
                    lis_row.append(x)
                    comp_row_score, hum_row_score = self.try_score(lis_row, row, comp_row_score,
                                                                   hum_row_score)
                    row = 1
                    if j == 6 and (board[i][j] != board[i][j - 1]):
                        x = (current, row)
                        lis_row.append(x)
                        comp_row_score, hum_row_score = self.try_score(lis_row, row, comp_row_score,
                                                                       hum_row_score)

            # if i == 5:
            #     prev = board[i][6 - 1]
            #     current = board[i][6]
            #     lis_row.append((current, row))
            #     comp_row_score, hum_row_score = self.try_score(row, comp_row_score, hum_row_score,
            #                                                    prev, current)
            # print(lis_row)
        comp_col_score = 0
        hum_col_score = 0
        for i in range(0, 7, 1):
            col = 1
            lis_col = []
            for j in range(1, 6, 1):

                if board[j][i] == board[j - 1][i]:
                    col += 1

                if (board[j][i] != board[j - 1][i]) or (
                        j == 5 and board[j][i] == board[j - 1][i]):
                    prev = board[j - 1][i]
                    current = board[j][i]
                    lis_col.append((prev, col))
                    comp_col_score, hum_col_score = self.try_score(lis_col, col, comp_col_score,
                                                                   hum_col_score)
                    col = 1
                    if j == 5 and board[j][i] != board[j - 1][i]:
                        lis_col.append((board[j][i], 1))
                        comp_col_score, hum_col_score = self.try_score(lis_col, col, comp_col_score,
                                                                       hum_col_score)

            # if i == 6:
            #     prev = board[5 - 1][i]
            #     current = board[5][i]
            #     lis_col.append((current, col))
            #     comp_col_score, hum_col_score = self.try_score(col, comp_col_score, hum_col_score,
            #                                                    prev, current)
            # print(lis_col)
        # print(comp_row_score)
        # print(comp_col_score)
        # print(hum_row_score)
        # print(hum_col_score)
        return comp_row_score + comp_col_score - hum_row_score - hum_col_score

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

    def try_score(self, lis, count, com_score, hum_score):
        i = 1
        index = len(lis) - i
        current = lis[index]
        counter = 0
        play_counter = 0
        play = '*'

        if current[0] == '1' or current[0] == '0':
            index -= 1
            counter = current[1]
            if counter >= 4 and current[0] == '1':
                return -1000000000000000000, 0
            elif counter >= 4 and current[0] == '0':
                return 10000000000000000000, 0
            play_counter = counter
            play = current[0]
            while index >= 0:
                if lis[index][0] == current[0] or lis[index][0] == '*':
                    counter += lis[index][1]
                    if lis[index][0] == current[0]:
                        play_counter += lis[index][1]
                else:
                    break
                index -= 1

        if current[0] == '*':
            play = 'null'
            index -= 1
            counter = current[1]
            if index >= 0:
                current = lis[index]
                play = current[0]
                while index > 0:
                    if lis[index][0] == current[0] or lis[index][0] == '*':
                        counter += lis[index][1]
                        if lis[index][0] == current[0]:
                            play_counter += lis[index][1]
                    else:
                        break
                    index -= 1

            #####
        # print(lis)
        # print(play)
        # print(counter)

        # if 0 <= (counter - play_counter) <= 4 and play == '0':
        #     return com_score + 1000000, 0
        #
        # if 0 <= (counter - play_counter) <= 4 and play == '1':
        #     return com_score - 1000000, 0

        return com_score  + 100000001, 0


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
    s.try_heuristic()
