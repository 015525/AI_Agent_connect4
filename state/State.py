# MTELFR = mask_to_extract_last_filled_row
# MTECS = mask_to_extract_column_state

class State:

    def __init__(self, state):
        self.state = state

    def get_neighbours(self, playerNum):
        neighbours = []
        for i in range(1,7):
            if self.valid_play(i):
                #print(self.update_state(i, playerNum))
                neighbours.append(self.update_state(i, playerNum))

        return neighbours

    def valid_play(self, colNum):
        MTELFR = 7
        MTELFR = MTELFR << ((colNum * 9) - 3)
        LastFilledRow = self.state & MTELFR
        LastFilledRow = LastFilledRow >> ((colNum * 9) - 3)
        if LastFilledRow < 6:
            return True
        return False

    def update_state(self, colNum, playerNum):
        temp_state = self.state
        MTELFR = 7
        MTECS = 63
        play = 1

        MTELFR = MTELFR << ((colNum*9)-3)
        LastFilledRow = temp_state & MTELFR
        LastFilledRow = LastFilledRow >> ((colNum*9)-3)

        MTECS = MTECS << ((colNum-1)*9)
        colState = temp_state & MTECS
        colState = colState >> ((colNum-1)*9)

        play = play << (6-LastFilledRow-1)
        play = ~play if playerNum == 0 else play

        if playerNum == 0:
            colState = colState & play
        else:
            colState = colState | play

        LastFilledRow += 1

        remainder = temp_state >> ((colNum * 9))
        remainder = remainder << ((colNum * 9))

        temp_state = temp_state | MTECS
        temp_state = ~ temp_state
        colState = ~ colState
        colState = colState << ((colNum - 1) * 9)
        #colState = colState << (54-(colNum*9) + 3)
        #colState = colState >> (54-(colNum*9) + 3)
        temp_state = temp_state | colState
        temp_state = ~ temp_state
        # self.state = self.state & colState

        temp_state = temp_state | MTELFR
        temp_state = ~ temp_state
        LastFilledRow = ~ LastFilledRow
        LastFilledRow = LastFilledRow << ((colNum * 9) - 3)
        #LastFilledRow = LastFilledRow << (54-(colNum*9))
        #LastFilledRow = LastFilledRow >> (54-(colNum*9))
        temp_state = temp_state | LastFilledRow
        temp_state = ~ temp_state
        #self.state = self.state & LastFilledRow

        temp_state = temp_state | remainder

        return temp_state

    def estimate_state(self):
        pass



if __name__ == "__main__" :
    s = State(12898978266014928)
    #print(s.state)
    #req_s = s.update_state(2, 0)
    #print(req_s)
    print(s.get_neighbours(1))
    pass

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




