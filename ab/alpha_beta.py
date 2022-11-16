import random
import sys
from state.State import State


class alphabeta:

    def __init__(self, maxDepth):
        self.maxDepth = maxDepth
        self.nextState = None

    def get_next_state(self, currentState):
        value, next_state = self._alpha_beta_pruning(currentState, self.maxDepth, True, float('-inf'),
                                                     sys.float_info.max)
        return next_state

    def _alpha_beta_pruning(self, state, depth, maxPlayer, alpha, beta):
        if depth == 0 or state.is_terminal():
            return state.get_heuristic(), None

        if maxPlayer:
            max_value = float('-inf')
            ss = state
            for child in state.get_neighbours(state.computer):
                value = self._alpha_beta_pruning(child, depth - 1, not maxPlayer, alpha, beta)[0]
                if max_value < value:
                    max_value = value
                    ss = child
                    alpha = value
                if beta <= alpha:
                    break
            return max_value, ss
        else:
            min_value = sys.float_info.max
            ss = state
            for child in state.get_neighbours(state.computer):
                value = self._alpha_beta_pruning(child, depth - 1, not maxPlayer, alpha, beta)[0]
                if min_value > value:
                    min_value = value
                    ss = child
                    beta = min_value
                if beta <= alpha:
                    break
            return min_value, ss
