from state.State import State, print_state

if __name__ == '__main__':

    s = State(6612116015251603087)
    print_state(s)
    print(s.is_terminal())
    # score_analysis = {
    #     "r1": 3, "r2": 2, "r3": 0, "r4": 0, "r5": 0, "r6": 0,
    #     "c1": 3, "c2": 2, "c3": 1, "c4": 0, "c5": 0, "c6": 0, "c7": 0,
    #     "rc37": 0, "rc27": 0, "rc17": 0, "rc16": 0, "rc15": 0, 'rc14': 0,
    #     "rc31": 0, "rc21": 0, "rc11": 0, "rc12": 0, "rc13": 0
    # }
    # score = 11
    # colNum = 4
    # playerNum = 1
    # score_analysis, score = s.get_new_score(score_analysis, score, colNum, 1)
    # print(score_analysis)
    # print(score)

