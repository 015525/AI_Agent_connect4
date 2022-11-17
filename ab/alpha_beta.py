import random
import sys

from treelib import Tree

from state.State import State


class alphabeta:

    def __init__(self, maxDepth):
        #print("max depth is " + str(maxDepth))
        self.maxDepth = maxDepth
        self.nextState = None
        self.tree = {}

    def get_next_state(self, currentState):
        self.tree = {}
        #print("depth im get next state is " + str(self.maxDepth))
        value, col = self._alpha_beta_pruning(currentState, self.maxDepth, True, float('-inf'),
                                                     sys.float_info.max)
        self.print_minimaxTree()
        return col

    def _alpha_beta_pruning(self, state, depth, maxPlayer, alpha, beta):
        #print("depth is ",depth)
        if depth == 0 or state.is_terminal():
            return state.get_heuristic(), None

        if maxPlayer:
            max_value = float('-inf')
            col = None
            curr_state_heurestic = state.get_heuristic()
            self.tree[str(state.state) + "@" + str(curr_state_heurestic)] = []
            for child in state.get_neighbours(state.computer):
                self.tree[str(state.state) + "@" + str(state.get_heuristic())].append(str(child.state) + "@" + str(child.get_heuristic()))
                max_value = self._alpha_beta_pruning(child, depth - 1, not maxPlayer, alpha, beta)[0]
                #self.tree[str(state.state) + "@" + str(curr_state_heurestic)].append(str(child.state) + "@" + str(max_value))
                if max_value >= beta:
                    break
                if max_value > alpha:
                    alpha = max_value
                    col = child.col_num
            return max_value, col
        else:
            min_value = sys.float_info.max
            col = None
            curr_state_heurestic = state.get_heuristic()
            self.tree[str(state.state) + "@" + str(curr_state_heurestic)] = []
            for child in state.get_neighbours(state.computer):
                self.tree[str(state.state) + "@" + str(state.get_heuristic())].append(str(child.state) + "@" + str(child.get_heuristic()))
                min_value = self._alpha_beta_pruning(child, depth - 1, not maxPlayer, alpha, beta)[0]
                #self.tree[str(state.state) + "@" + str(curr_state_heurestic)].append(str(child.state) + "@" + str(min_value))
                if min_value <= alpha:
                    break
                if min_value < beta:
                    beta = min_value
                    col = child.col_num
            return min_value, col


    def print_minimaxTree(self):
        nodes = self.tree.keys()  # all nodes in the tree
        # firstKey = self.tree.keys()[0]
        tree = Tree()
        tree.create_node(f"{list(nodes)[0]}", f"{list(nodes)[0]}")  # root node
        for i in nodes:  # range(1, len(nodes)):
            for j in self.tree[i]:
                # print(type(i), type(j))
                try:
                    tree.create_node(f"{j}", f"{j}", parent=f"{i}")
                except:
                    continue

        print("shown tree is  : ")
        tree.show()
