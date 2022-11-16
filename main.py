from minimax.MiniMax import MiniMax
from state.State import State


def print_game_path(state):
    print("*********************** Path of the Game ***********************")
    while state.child is not None:
        state.print_state()
        state = state.child
        print("\n")


if __name__ == '__main__':
    # current_state = State(6521938056733407885)
    current_state = State(6485768453102907528)
    first_state = current_state
    player = False
    alg = MiniMax(5)
    while True:
        current_state.print_state()
        if current_state.is_terminal():
            break

        if player:
            player = False
            next_s = alg.get_next_state(current_state)
            next_s.computer_score = next_s.get_new_score(next_s.col_num, State.computer)
            # next_s.parent = current_state
            current_state = next_s
        else:
            player = True
            col = int(input("Enter column number: "))
            next_s = current_state.update_state(col, State.human)
            next_s.human_score = next_s.get_new_score(col, State.human)
            next_s.parent = current_state
            current_state = next_s
            current_state.col_num = col

    # print_game_path(first_state)

