import sys


class MiniMax:
    dic = {}

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.next_state = None
        self.tree = {}

    def get_next_state(self, current_state):
        val, next_state = self._minimax(current_state, self.max_depth, True)
        return next_state

    def _minimax(self, state, depth, MaximizingPlayer):
        if depth == 0 or state.is_terminal():
            return state.get_heuristic(), None

        if MaximizingPlayer:
            value = float('-inf')
            neighbours = state.get_neighbours(state.computer)
            self.neighbours = neighbours
            ss = None
            for child in neighbours:
                max = self._minimax(child, depth - 1, False)[0]
                if max > value:
                    value = max
                    ss = child
            return value, ss

        else:
            value = sys.float_info.max
            neighbours = state.get_neighbours(state.human)
            self.neighbours = neighbours
            ss = None
            for child in neighbours:
                min = self._minimax(child, depth - 1, True)[0]
                if min < value:
                    value = min
                    ss = child

        return value, ss
