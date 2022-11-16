from minimax.MiniMax import MiniMax
from state.State import State
from ab.alpha_beta import alphabeta

if __name__ == '__main__':
    current_state = State(6485768453102907528)
    first_state = current_state
    player = False
    # alg = MiniMax(4)
    alg = alphabeta(8)

    while True:

        current_state.print_state()
        if current_state.is_terminal():
            break

        if player:
            player = False
            next_s = alg.get_next_state(current_state)
            current_state = next_s
        else:
            player = True
            col = int(input("Enter column number: "))
            next_s = current_state.update_state(col, State.human)
            current_state = next_s
