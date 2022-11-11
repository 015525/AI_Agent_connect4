import sys

from state.State import print_state


class MiniMax:

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.next_state = None
        self.tree = {}

    def get_next_state(self, current_state):
        # ????????????????????????????
        val, next_state = self._minimax(current_state, self.max_depth, True)
        next_state.heuristic_score = val
        # ????????????????????????????
        return next_state

    def _minimax(self, state, depth, MaximizingPlayer):
        if depth == 0 or state.is_terminal():
            return state.get_total_heuristic(), state

        if MaximizingPlayer:
            value = sys.float_info.min
            neighbours = state.get_neighbours(state.computer)
            for child in neighbours:
                child.parent = state
                max, temp = self._minimax(child, depth - 1, False)
                next_state = child
                if max > value:
                    value = max
                    next_state = child
            return value, next_state
        else:
            value = sys.float_info.max
            neighbours = state.get_neighbours(state.human)
            for child in neighbours:
                child.parent = state
                min, temp = self._minimax(child, depth - 1, True)
                next_state = child
                if min < value:
                    value = min
                    next_state = child

            return value, next_state
