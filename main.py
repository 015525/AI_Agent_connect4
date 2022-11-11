from minimax.MiniMax import MiniMax
from state.State import State, print_state

if __name__ == '__main__':
    current_state = State(6521938056733407885)
    print_state(current_state)
    player = False
    alg = MiniMax(7)
    while True:
        if player:
            player = False
            alg.get_next_state(current_state)
        else:
            player = True
            col = int(input("Enter column number: "))
            current_state = current_state.update_state(col, 1)

        print_state(current_state)
