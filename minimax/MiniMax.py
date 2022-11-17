import sys

from treelib import Tree

from state.State import State


class MiniMax:
    dic = {}
    #tree = {}

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.next_state = None
        self.tree = {}

    def get_next_state(self, current_state):
        self.tree = {}
        val, col = self._minimax(current_state, self.max_depth, True)
        self.print_minimaxTree()
        return col

    def _minimax(self, state, depth, MaximizingPlayer):
        if depth == 0 or state.is_terminal():

            return state.get_heuristic(), None

        if MaximizingPlayer:
            value = float('-inf')
            neighbours = state.get_neighbours(state.computer)
            self.neighbours = neighbours
            col = None
            curr_state_heurestic = state.get_heuristic()
            self.tree[str(state.state) + "@" + str(curr_state_heurestic)] = []
            for child in neighbours:
                self.tree[str(state.state) + "@" + str(state.get_heuristic())].append(str(child.state) + "@" + str(child.get_heuristic()))
                max = self._minimax(child, depth - 1, False)[0]
                #self.tree[str(state.state) + "@" + str(curr_state_heurestic)].append(str(child.state) + "@" + str(max))
                if max > value:
                    value = max
                    col = child.col_num
            return value, col

        else:
            value = sys.float_info.max
            neighbours = state.get_neighbours(state.human)
            self.neighbours = neighbours
            col = None
            curr_state_heurestic = state.get_heuristic()
            self.tree[str(state.state) + "@" + str(curr_state_heurestic)] = []
            for child in neighbours:
                self.tree[str(state.state) + "@" + str(state.get_heuristic())].append(str(child.state) + "@" + str(child.get_heuristic()))
                min = self._minimax(child, depth - 1, True)[0]
                #self.tree[str(state.state) + "@" + str(curr_state_heurestic)].append(str(child.state) + "@" + str(min))
                if min < value:
                    value = min
                    col = child.col_num

        return value, col

    def print_minimaxTree(self):
        nodes = self.tree.keys()# all nodes in the tree
        #firstKey = self.tree.keys()[0]
        tree = Tree()
        tree.create_node(f"{list(nodes)[0]}", f"{list(nodes)[0]}") # root node
        for i in nodes: #range(1, len(nodes)):
            for j in self.tree[i]:
                #print(type(i), type(j))
                try:
                    tree.create_node(f"{j}", f"{j}", parent=f"{i}")
                except:
                    continue

        print("shown tree is  : ")
        tree.show()



