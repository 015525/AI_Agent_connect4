import sys


class MiniMax:

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.next_state = None
        self.tree = {}

    def get_next_state(self, current_state):
        self._minimax(current_state, self.max_depth, True)
        return self.next_state

    def _minimax(self, state, depth, MaximizingPlayer):
        if depth == 0 or state.is_terminal():
            return state.get_heutrestic()

        if MaximizingPlayer:
            value = sys.float_info.min
            neighbours = state.get_neighbours(state.computer)
            for child in neighbours:
                # ????????????????????
                self.tree[child] = state.state
                max = self._minimax(child, depth - 1, False)
                if max > value:
                    value = max
                    self.next_state = child
            return value
        else:
            value = sys.float_info.max
            neighbours = state.get_neighbours(state.human)
            for child in neighbours:
                # ???????????????????? 
                self.tree[child] = state.state
                min = self._minimax(child, depth - 1, True)
                if min < value:
                    value = min
                    self.next_state = child

            return value
