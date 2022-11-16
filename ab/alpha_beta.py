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
                max_value = self._alpha_beta_pruning(child, depth - 1, not maxPlayer, alpha, beta)[0]
                if max_value >= beta:
                    break
                if max_value > alpha:
                    alpha = max_value
                    ss = child
            return max_value, ss
        else:
            min_value = sys.float_info.max
            ss = state
            for child in state.get_neighbours(state.computer):
                min_value = self._alpha_beta_pruning(child, depth - 1, not maxPlayer, alpha, beta)[0]
                if min_value <= alpha:
                    break
                if min_value < beta:
                    ss = child
                    beta = min_value
            return min_value, ss
