# MTELFR = mask_to_extract_last_filled_row
# MTECS = mask_to_extract_column_state
# assume column start with 1
# assume binary representation starts from right
# each column is represented by 9 bits 3 for last filled row in the column 6 for the plays in the column
# the 3 bits of the last filled row in the column also are at the right of the 9 bits
# the 6 bits of the play the first play (row 1) is the first bit from the right

class State:
    score_analysis = {
                      "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
                      "c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
                      "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0,
                      "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
                      }

    def __init__(self, state):
        self.state = state

    def get_neighbours(self, playerNum):
        neighbours = []
        for i in range(1,8):
            if self.valid_play(i):
                #print(self.update_state(i, playerNum))
                neighbours.append(self.update_state(i, playerNum))
                #print(neighbours[i-c].state)


        return neighbours

    def valid_play(self, colNum):
        MTELFR = 7
        MTELFR = MTELFR << ((colNum -1)* 9)
        LastFilledRow = self.state & MTELFR
        LastFilledRow = LastFilledRow >> ((colNum-1) * 9)
        if LastFilledRow < 6:
            return True
        return False

    def update_state(self, colNum, playerNum):
        temp_state = State(self.state)
        MTELFR = 7
        MTECS = 63
        play = 1

        MTELFR = MTELFR << ((colNum-1)*9)
        LastFilledRow = temp_state.state & MTELFR
        LastFilledRow = LastFilledRow >> ((colNum-1)*9)

        #if LastFilledRow == 6 : return None

        MTECS = MTECS << ((colNum-1)*9 + 3)
        colState = temp_state.state & MTECS
        colState = colState >> ((colNum-1)*9 + 3)

        play = play << (LastFilledRow)
        play = ~play if playerNum == 0 else play

        if playerNum == 0:
            colState = colState & play
        else:
            colState = colState | play

        LastFilledRow += 1


        remainder = temp_state.state >> ((colNum * 9))
        remainder = remainder << ((colNum * 9))

        temp_state.state = temp_state.state | MTELFR
        temp_state.state = ~ temp_state.state
        LastFilledRow = ~ LastFilledRow
        LastFilledRow = LastFilledRow << ((colNum-1) * 9)
        # LastFilledRow = LastFilledRow << (54-(colNum*9))
        # LastFilledRow = LastFilledRow >> (54-(colNum*9))
        temp_state.state = temp_state.state | LastFilledRow
        temp_state.state = ~ temp_state.state
        # self.state = self.state & LastFilledRow

        temp_state.state = temp_state.state | MTECS
        temp_state.state = ~ temp_state.state
        colState = ~ colState
        colState = colState << ((colNum - 1) * 9 + 3)
        #colState = colState << (54-(colNum*9) + 3)
        #colState = colState >> (54-(colNum*9) + 3)
        temp_state.state = temp_state.state | colState
        temp_state.state = ~ temp_state.state
        # self.state = self.state & colState

        temp_state.state = temp_state.state | remainder

        return temp_state

    def update_score(self):
        pass

    def estimate_state(self):
        pass



if __name__ == "__main__" :
    s = State(679293331470573)
    print(s.state)
    req_s = s.update_state(7, 1)
    print(req_s.state)
    list_of_neighbours = s.get_neighbours(1)
    print("===============================")
    for i in (list_of_neighbours):
        print(i.state)

#[12898978266014996, 12898978266048208, 12898978286986448, 12903513751479504, 15185962451789008]
#current state 143800
# player num is 0
# col num is 2
# required output is 176568

#current state 143800
# player num is 1
# col num is 2
# required output is 177592

#current state 12898978266014928
# player num is 0
# col num is 6
# required output is 15150778079700176

#current state 12898978266014928
# player num is 1
# col num is 6
# required output is 15185962451789008

#current state 12898978266014928
# player num is 0
# col num is 2
# required output is 12898978266047696

#current state 12898978266014928
# player num is 1
# col num is 2
# required output is 12898978266048208

#18014398509481984 # 1 with 54 zero after it in binary
#9007199254740992  # 1 with 53 zero after it in binary

#new form
#000010011010011101000001001101101110000111100011101101
#679293331470573
#colnum 1 player 1
#679293331470830




