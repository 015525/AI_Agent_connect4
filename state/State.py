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
    score_analysis = {
        "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
        "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
        "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0, 'rc14': 0,
        "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
    }

    def __init__(self, state):
        self.parent = None
        self.state = state
        self.computer_score = 0
        self.human_score = 0
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
        #temp_state.parent = self

        return temp_state

    # this is called after the new state is updated
    def get_new_score(self, col_num, player_num):
        # ????????????????????????????????
        if self.parent is None:
            score = 0
        else:
            if player_num == State.computer:
                score = self.parent.computer_score
            else:
                score = self.parent.human_score
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
        sideRow1rowAllowed = True

        for i in range(start, 8):
            if 8-start < 4 :
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
        sideRow2rowAllowed = True

        for i in range(start, 0, -1):
            if start-0 < 4 :
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

        # print(points_from_row)
        # print(points_from_column)
        # print(points_from_sideRow1)
        # print(points_from_sideRow2)
        points_from_row -= State.score_analysis['r' + str(LastFilledRow)]
        points_from_column -= State.score_analysis['c' + str(col_num)]
        if sideRow1row < 4 and sideRow1rowAllowed:
            points_from_sideRow1 -= State.score_analysis['rc' + str(sideRow1row) + str(sideRow1col)]
        if sideRow2row < 4 and sideRow2rowAllowed:
            points_from_sideRow2 -= State.score_analysis['rc' + str(sideRow2row) + str(sideRow2col)]

        score += points_from_row + points_from_column + points_from_sideRow2 + points_from_sideRow1

        State.score_analysis['r' + str(LastFilledRow)] += points_from_row
        State.score_analysis['c' + str(col_num)] += points_from_column
        if sideRow1row < 4 and sideRow1rowAllowed:
            State.score_analysis['rc' + str(sideRow1row) + str(sideRow1col)] += points_from_sideRow1
        if sideRow2row < 4 and sideRow2rowAllowed:
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

    def get_total_heuristic(self, score1, score2, heuristic_analysis_human, heuristic_analysis_computer,
                            heurestic_score_human, heurestic_score_computer):
        # ???? not sure??????????????????????????????????
        # And computer_score and human_score can be used instead ???????
        #score1 = self.get_new_score(self.col_num, State.computer)
        #score2 = self.get_new_score(self.col_num, State.human)
        # ???? not sure??????????????????????????????????



        if not score1:
            score1 = 0.125 * score2
        if not score2:
            score2 = 0.125 * score1

        if not score1 and not score2 :
            score1 = score2 = 1

        score1Rat= score1 / (score2+score1)
        score2Rat = score2 / (score2 + score1)

        heuristic_analysis1, heuristic_score1 = self.get_heuristic(self.col_num,
                                                                   State.human, heuristic_analysis_human, heurestic_score_human)

        print("=======================================")
        heuristic_analysis2, heuristic_score2 = self.get_heuristic(self.col_num,
                                                                   State.computer, heuristic_analysis_computer, heurestic_score_computer)
        total_heuristic = score1Rat * heuristic_score1 - score2Rat * heuristic_score2
        print(heuristic_analysis1)
        print(heuristic_analysis2)
        print(heuristic_score1)
        print(heuristic_score2)
        #print(total_heuristic)
        return total_heuristic

    def get_heuristic(self, col_num, player_num, heuristic_analysis, heuristic_score):
        '''
        if self.parent is None:
            temp_heuristic_analysis = self.heuristic_analysis
            heuristic_score = 0
        else:
            temp_heuristic_analysis = self.parent.heuristic_analysis
            heuristic_score = self.parent.heuristic_score
        '''
        temp_heuristic_analysis = heuristic_analysis

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
                #print("last filled row is ", LastFilledCRow)
                continue

            c = self.get_play(cState, LastFilledRow)
            if c == player_num:
                counter += 1
                points_from_row = counter
            else:
                # if i > 4 and counter >= 3 and counter != i :
                if i - opponent_counter > 4 and counter > 0:
                    print("second i now is ", i)
                    points_from_row = counter
                    break
                else:
                    print("i now is " , i)
                    points_from_row = 0
                opponent_counter += 1
                counter = 0
                if 8-i < 4:
                    break

            '''
            if counter:
                points_from_row += counter
                counter -= 1
            '''

        #print("entered and points from row is ", points_from_row)
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
        sideRow1rowAllowed = True

        for i in range(start, 8):
            if 8-start < 4 :
                sideRow1rowAllowed = False
                break
            LastFilledCRow, cState = self.get_last_col_and_state(i)

            if LastFilledCRow < play_to_get:
                play_to_get += 1
                continue

            c = self.get_play(cState, play_to_get)
            print("cstate now is ", cState)
            play_to_get += 1
            if c == player_num:
                counter += 1
                points_from_sideRow1 = counter
            else:
                # if i > 4 and counter >= 3 and counter != i :
                if i - opponent_counter > 4 and counter > 0:
                    print("enter and i is", i)
                    points_from_sideRow1 = counter
                    break
                else:
                    points_from_sideRow1 = 0

                opponent_counter += 1
                counter = 0
                if 8-i < 4 :
                    break

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
        sideRow2rowAllowed = True

        for i in range(start, 0, -1):
            if start-0 < 4 :
                sideRow2rowAllowed = False
                break
            LastFilledCRow, cState = self.get_last_col_and_state(i)

            if LastFilledCRow < play_to_get:
                play_to_get += 1
                continue

            c = self.get_play(cState, play_to_get)
            play_to_get += 1
            if c == player_num:
                counter += 1
                points_from_sideRow2 = counter
            else:
                # if i > 4 and counter >= 3 and counter != i :
                if i - opponent_counter > 4 and counter > 0:
                    points_from_sideRow2 = counter
                    break
                else:
                    points_from_sideRow2 = 0

                opponent_counter += 1
                counter = 0
                if i< 4 :
                    break

            if play_to_get > 6:
                break

        print(points_from_row)
        print(points_from_column)
        print(points_from_sideRow1)
        print(points_from_sideRow2)
        points_from_row -= temp_heuristic_analysis['r' + str(LastFilledRow)]
        points_from_column -= temp_heuristic_analysis['c' + str(col_num)]

        print("side row 1 row is ", sideRow1row, "side row 1 col", sideRow1col)
        print("side row 2 row is ", sideRow2row, "side row 2 col", sideRow2col)

        if sideRow1row < 4 and sideRow1rowAllowed:
            points_from_sideRow1 -= temp_heuristic_analysis['rc' + str(sideRow1row) + str(sideRow1col)]
        if sideRow2row < 4 and sideRow2rowAllowed:
            points_from_sideRow2 -= temp_heuristic_analysis['rc' + str(sideRow2row) + str(sideRow2col)]

        heuristic_score += (points_from_row + points_from_column + points_from_sideRow2 + points_from_sideRow1)

        temp_heuristic_analysis['r' + str(LastFilledRow)] += points_from_row
        temp_heuristic_analysis['c' + str(col_num)] += points_from_column
        if sideRow1row < 4 and sideRow1rowAllowed:
            temp_heuristic_analysis['rc' + str(sideRow1row) + str(sideRow1col)] += points_from_sideRow1
        if sideRow2row < 4 and sideRow2rowAllowed:
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
    s = State(162165389432717312)
    s.col_num = 5

    heuristic_analysis_human = {
        "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
        "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 1,
        "rc37": 0, "rc27": 0, "rc17": 1, "rc16": 0, "rc15": 0, 'rc14': 0,
        "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
    }

    heuristic_analysis_computer = {
        "r1": 1, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
        "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 1, "c7": 0,
        "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 1, "rc15": 0, 'rc14': 0,
        "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
    }


    heurestic_score  = s.get_total_heuristic(0,0, heuristic_analysis_human, heuristic_analysis_computer, 2, 3)
    #print(new_heurestic_analysis)
    print(heurestic_score)
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

#heurestic test
#positive heurestic means for human negative means for computer

'''
heuristic_analysis_human = {
            "r1": 3, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 1, "c5": 0, "c6": 0, "c7": 1,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 1, "rc15": 1, 'rc14': 1,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 1, "rc13": 0
        }

#expected new human heurestic      
heuristic_analysis_human = {
            "r1": 4, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 1, "c4": 1, "c5": 0, "c6": 0, "c7": 1,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 1, "rc15": 1, 'rc14': 1,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 1, "rc13": 0
        }
        
heuristic_analysis_computer = {
            "r1": 0, "r2": 1, "r3": 1, "r4": 0, "r5": 0, "r6": 0,
            "c1": 1, "c2": 1, "c3": 0, "c4": 0, "c5": 1, "c6": 2, "c7": 1,
            "rc37": 0, "rc27": 0, "rc17": 2, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 2, "rc12": 1, "rc13": 1
        }

#expected new computer heurestic      
heuristic_analysis_computer = {
            "r1": 0, "r2": 1, "r3": 1, "r4": 0, "r5": 0, "r6": 0,
            "c1": 1, "c2": 1, "c3": 0, "c4": 0, "c5": 1, "c6": 2, "c7": 1,
            "rc37": 0, "rc27": 0, "rc17": 2, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 2, "rc12": 1, "rc13": 1
        }
        
old heurestic : -1.5
expected new heurestic : 8.44444

old score_human : 0 old score_computer : 0
new score_human : 1 new score_computer : 0


new state 
162201811965711361
in binary 
1001000000010000011011000001001000001001000001010000000001

play was for human (3) in col 3
'''

'''
heuristic_analysis_human = {
            "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 1,
            "rc37": 0, "rc27": 0, "rc17": 1, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }

#expected new human heurestic      
heuristic_analysis_human = {
            "r1": 1, "r2": 1, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 2,
            "rc37": 0, "rc27": 1, "rc17": 1, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }

heuristic_analysis_computer = {
            "r1": 1, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 1, "c7": 0,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 1, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }

#expected new computer heurestic      
heuristic_analysis_computer = {
            "r1": 1, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 1, "c7": 0,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 1, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }

old heurestic : 0
expected new heurestic : 1.5

old score_human : 0 old score_computer : 0
new score_human : 0 new score_computer : 0

old heurestic_human : 3 old heurestic_computer : 3
new heurestic_human : 6 new heurestic_computer : 3

new state 
468409545618620416
in binary 
11010000000001000000000000000000000000000000000000000000000

play was for human (1) in col 7
'''

'''
heuristic_analysis_human = {
            "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 1,
            "rc37": 0, "rc27": 0, "rc17": 1, "rc16": 0, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }

#expected new human heurestic      
heuristic_analysis_human = {
            "r1": 1, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 1, "c6": 0, "c7": 1,
            "rc37": 0, "rc27": 0, "rc17": 1, "rc16": 0, "rc15": 1, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }

heuristic_analysis_computer = {
            "r1": 1, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 1, "c7": 0,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 1, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }

#expected new computer heurestic      
heuristic_analysis_computer = {
            "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
            "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 1, "c7": 0,
            "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 1, "rc15": 0, 'rc14': 0,
            "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
        }

old heurestic : -0.5
expected new heurestic : 1.5

old score_human : 0 old score_computer : 0
new score_human : 0 new score_computer : 0

old heurestic_human : 2 old heurestic_computer : 3
new heurestic_human : 5 new heurestic_computer : 2


new state 
162165389432717312
in binary 
1001000000001000001001000000000000000000000000000000000000

play was for human (1) in col 5
'''
