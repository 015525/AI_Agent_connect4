import sys
from state.State import print_state, State


class MiniMax:
    dic = {}

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.next_state = None
        self.tree = {}

    def get_next_state(self, current_state):
        # ????????????????????????????
        val, col = self._minimax(current_state, self.max_depth, True)
        next_state = current_state
        next_state = next_state.update_state(col, State.computer)
        next_state.col_num = col
        # ????????????????????????????
        return next_state

    def _minimax(self, state, depth, MaximizingPlayer):
        if depth == 0 or state.is_terminal():
            return state.get_total_heuristic(), None

        if MaximizingPlayer:
            value = float('-inf')
            col = state.get_valid_col()
            neighbours = state.get_neighbours(state.computer)
            for child in neighbours:
                child.parent = state
                child.get_total_heuristic()
                max = self._minimax(child, depth - 1, False)[0]
                if max > value:
                    value = max
                    col = child.col_num
            return value, col

        else:
            value = sys.float_info.max
            col = state.get_valid_col()
            neighbours = state.get_neighbours(state.human)
            for child in neighbours:
                child.parent = state
                child.get_total_heuristic()
                min = self._minimax(child, depth - 1, True)[0]
                if min < value:
                    value = min
                    col = child.col_num
            return value, col
