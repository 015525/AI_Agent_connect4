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


def print_state(state):
    temp_state = state.state
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

    print(np.matrix(board))


class State:
    computer = 0
    human = 1
    last_human_col = -1
    score_analysis = {
        "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
        "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
        "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0, 'rc14': 0,
        "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
    }

    def __init__(self, state):
        self.parent = None
        self.state = state
        self.score = 0
        self.child = None
        self.heuristic_analysis = {
            "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }
        self.heuristic_score = 0
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

        return temp_state

    # this is called after the new state is updated
    def get_new_score(self, col_num, player_num):
        # ????????????????????????????????
        if self.parent is None:
            score = 0
        else:
            score = self.parent.score
        # ????????????????????????????????

        LastFilledRow, colState = self.get_last_col_and_state(col_num)
        # get points generated from column
        pointMask = 15
        points_from_column = 0
        if not player_num: colState = ~ colState
        for i in range(LastFilledRow - 3):  # max iterations is 3
            temp = pointMask & colState
            if temp == pointMask:
                points_from_column += 1
            pointMask = pointMask << 1

        # get points generated from row
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

        # get points generated from side row 1
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

        for i in range(start, 8):
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

        # get points generated from side row 2
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

        for i in range(start, 0, -1):
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

        # print(points_from_row)
        # print(points_from_column)
        # print(points_from_sideRow1)
        # print(points_from_sideRow2)
        points_from_row -= State.score_analysis['r' + str(LastFilledRow)]
        points_from_column -= State.score_analysis['c' + str(col_num)]
        if sideRow1row < 4:
            points_from_sideRow1 -= State.score_analysis['rc' + str(sideRow1row) + str(sideRow1col)]
        if sideRow2row < 4:
            points_from_sideRow2 -= State.score_analysis['rc' + str(sideRow2row) + str(sideRow2col)]

        score += points_from_row + points_from_column + points_from_sideRow2 + points_from_sideRow1

        State.score_analysis['r' + str(LastFilledRow)] += points_from_row
        State.score_analysis['c' + str(col_num)] += points_from_column
        if sideRow1row < 4:
            State.score_analysis['rc' + str(sideRow1row) + str(sideRow1col)] += points_from_sideRow1
        if sideRow2row < 4:
            State.score_analysis['rc' + str(sideRow2row) + str(sideRow2col)] += points_from_sideRow2

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

    def get_total_heuristic(self):
        # ???? not sure??????????????????????????????????
        score1 = self.get_new_score(self.col_num, State.computer)
        score2 = self.get_new_score(self.col_num, State.human)
        # ???? not sure??????????????????????????????????

        heuristic_analysis1, heuristic_score1 = self.get_heuristic(self.col_num,
                                                                   State.computer)
        heuristic_analysis2, heuristic_score2 = self.get_heuristic(self.col_num,
                                                                   State.human)
        total_heuristic = score1 * heuristic_score1 - score2 * heuristic_score2
        return total_heuristic

    def get_heuristic(self, col_num, player_num):
        if self.parent is None:
            temp_heuristic_analysis = self.heuristic_analysis
            heuristic_score = 0
        else:
            temp_heuristic_analysis = self.parent.heuristic_analysis
            heuristic_score = self.parent.heuristic_score

        LastFilledRow, colState = self.get_last_col_and_state(col_num)
        # get points generated from column
        pointMask = 1
        points_from_column = 0
        if not player_num: colState = ~ colState
        for i in range(LastFilledRow):
            temp = pointMask & colState
            if temp == pointMask:
                points_from_column += 1
            else:
                points_from_column = 0
                break
            pointMask = pointMask << 1
            pointMask += 1

        # get points generated from row
        points_from_row = 0
        counter = 0
        opponent_counter = 0
        for i in range(1, 8):
            LastFilledCRow, cState = self.get_last_col_and_state(i)
            if LastFilledCRow < LastFilledRow:
                continue

            c = self.get_play(cState, LastFilledRow)
            if c == player_num:
                counter += 1
                points_from_row = counter
            else:
                opponent_counter += 1
                # if i > 4 and counter >= 3 and counter != i :
                if i - opponent_counter > 4 and counter > 0:
                    points_from_row = counter
                    break
                else:
                    points_from_row = 0
                counter = 0

            '''
            if counter:
                points_from_row += counter
                counter -= 1
            '''

        # get points generated from side row 1
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

        for i in range(start, 8):
            LastFilledCRow, cState = self.get_last_col_and_state(i)

            if LastFilledCRow < play_to_get:
                continue

            c = self.get_play(cState, play_to_get)
            play_to_get += 1
            if c == player_num:
                counter += 1
                points_from_row = counter
            else:
                opponent_counter += 1
                # if i > 4 and counter >= 3 and counter != i :
                if i - opponent_counter > 4 and counter > 0:
                    points_from_row = counter
                    break
                else:
                    points_from_row = 0
                counter = 0

            if play_to_get > 6:
                break

        # get points generated from side row 2
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

        for i in range(start, 0, -1):
            LastFilledCRow, cState = self.get_last_col_and_state(i)

            if LastFilledCRow < play_to_get:
                continue

            c = self.get_play(cState, play_to_get)
            play_to_get += 1
            if c == player_num:
                counter += 1
                points_from_row = counter
            else:
                opponent_counter += 1
                # if i > 4 and counter >= 3 and counter != i :
                if i - opponent_counter > 4 and counter > 0:
                    points_from_row = counter
                    break
                else:
                    points_from_row = 0
                counter = 0

            if play_to_get > 6:
                break

        # print(points_from_row)
        # print(points_from_column)
        # print(points_from_sideRow1)
        # print(points_from_sideRow2)
        points_from_row -= temp_heuristic_analysis['r' + str(LastFilledRow)]
        points_from_column -= temp_heuristic_analysis['c' + str(col_num)]
        if sideRow1row < 4:
            points_from_sideRow1 -= temp_heuristic_analysis['rc' + str(sideRow1row) + str(sideRow1col)]
        if sideRow2row < 4:
            points_from_sideRow2 -= temp_heuristic_analysis['rc' + str(sideRow2row) + str(sideRow2col)]

        heuristic_score += points_from_row + points_from_column + points_from_sideRow2 + points_from_sideRow1

        temp_heuristic_analysis['r' + str(LastFilledRow)] += points_from_row
        temp_heuristic_analysis['c' + str(col_num)] += points_from_column
        if sideRow1row < 4:
            temp_heuristic_analysis['rc' + str(sideRow1row) + str(sideRow1col)] += points_from_sideRow1
        if sideRow2row < 4:
            temp_heuristic_analysis['rc' + str(sideRow2row) + str(sideRow2col)] += points_from_sideRow2

        self.heuristic_analysis = temp_heuristic_analysis
        self.heuristic_score = heuristic_score
        return temp_heuristic_analysis, heuristic_score

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


if __name__ == "__main__":
    s = State(6521938056733407885)
    #  score_analysis = {
    #     "r1": 3, "r2": 2, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
    #     "c1": 3, "c2": 2, "c3": 1, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
    #     "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0, 'rc14': 0,
    #     "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
    # }
    # sc = s.get_new_score(11, 4, 1)
    # print(State.score_analysis)
    # print(sc)
    '''
    s = State(679293331470573)
    print(s.state)
    mask = 7
    mask << 1
    print(mask)
    '''
    # print(30 & 31)
    # req_s = s.update_state(7, 1)
    # print(req_s.state)
    # list_of_neighbours = s.get_neighbours(1)
    # print("===============================")
    # for i in (list_of_neighbours):
    #    print(i.state)

# [12898978266014996, 12898978266048208, 12898978286986448, 12903513751479504, 15185962451789008]
# current state 143800
# player num is 0
# col num is 2
# required output is 176568

# current state 143800
# player num is 1
# col num is 2
# required output is 177592

# current state 12898978266014928
# player num is 0
# col num is 6
# required output is 15150778079700176

# current state 12898978266014928
# player num is 1
# col num is 6
# required output is 15185962451789008

# current state 12898978266014928
# player num is 0
# col num is 2
# required output is 12898978266047696

# current state 12898978266014928
# player num is 1
# col num is 2
# required output is 12898978266048208

# 18014398509481984 # 1 with 54 zero after it in binary
# 9007199254740992  # 1 with 53 zero after it in binary

# new form
# 000010011010011101000001001101101110000111100011101101
# 679293331470573
# colnum 1 player 1
# 679293331470830

# 8524845814331
