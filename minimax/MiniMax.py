import sys


class MiniMax:

    def minimax(self, state, depth, MaximizingPlayer):
        if depth == 0 or state.is_terminal():
            return state.get_heutrestic()

        if MaximizingPlayer:
            value = sys.float_info.min
            neighbours = state.get_neighbours()
            for child in neighbours:
                value = max(value, self.minimax(child, depth - 1, False))
            return value
        else:
            value = sys.float_info.max
            neighbours = state.get_neighbours()
            for child in neighbours:
                value = min(value, self.minimax(child, depth - 1, True))

        return value
