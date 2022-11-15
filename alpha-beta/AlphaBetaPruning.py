import random
import sys
from state.State import State
class AlphaBetaPruning:
    def __int__(self, maxDepth):
        self.maxDepth = maxDepth
        self.nextState = None
    def getNextState(self, currentState):
        print()
        value, next_state = self._alpha_beta_pruning(currentState, self.maxDepth, True, float('-inf'), sys.float_info.max)
        # @Mahmoud Gad: do what you want here
    def _alpha_beta_pruning(self, state, depth, maxPlayer, alpha, beta):
        if depth == 0 or state.is_terminal():
            print()
            # this is alpha-beta should do
            #  get heuristic values and compare it alpha, beta according to the current palyer
            # @Mahmoud Gad: edit it to run with the state
            """
            values = node.values
            for value in values:
                if alpha > beta:
                    print("Pruning")
                    break
                if maxPlayer:
                    if value > node.value:
                        node.value = value
                        path.insert(depth, {node: node.value})
                    alpha = max(alpha, value)
                else:
                    if value < node.value:
                        node.value = value
                        path.insert(depth, {node: node.value})
                    beta = max(beta, value)
               # @Mahmoud Gad: after finishing the code above you should 
               #                return node.value 'or alpha but i test it and found node.value is best according to alpha-beta-practice site', and NULL or node as you like
            """
        if maxPlayer:
            value = float('-inf')
            ss = state
            for child in state.get_neighbours(state.computer):
                child.parent = state
                # @Mahmoud Gad: check this line
                #child.get_total_heuristic()
                max = self._alpha_beta_pruning(child, depth-1, not maxPlayer, alpha, beta)[0]
                if max > value:
                    value = max
                    ss = child
            return value, ss
        else:
            value = sys.float_info.max
            ss = state
            for child in state.get_neighbours(state.computer):
                # @Mahmoud Gad: check this line
                # child.get_total_heuristic()
                min = self._alpha_beta_pruning(child, depth - 1, not maxPlayer, alpha, beta)[0]
                if min < value:
                    value = min
                    ss = child
            return value, ss

# @Mahmoud Gad: the next code for testing purposes
class Node:
    def __init__(self, v, values, r):
        self.value = v
        self.values = values
        self.children = []
        self.random = r
    def addChild(self, node):
        self.children.append(node)
path = [{}]
def createTree():
    root = Node(minusInfinity, [], 0)
    root.addChild(Node(infinity, [], 1))
    root.addChild(Node(infinity, [], 2))
    #root.addChild(Node(infinity, []))
    root.children[0].addChild(Node(minusInfinity, [-3, 18], 3))
    root.children[0].addChild(Node(minusInfinity, [15, 2], 4))
    #root.children[0].addChild(Node(minusInfinity, [-2, -8, 13]))
    root.children[1].addChild(Node(minusInfinity, [-15, 19], 5))
    root.children[1].addChild(Node(minusInfinity, [1, 19], 6))
    #root.children[1].addChild(Node(minusInfinity, [11, 1, -13]))
    #root.children[2].addChild(Node(minusInfinity, [20, 20, -12]))
    #root.children[2].addChild(Node(minusInfinity, [-12, 0, -6]))
    #root.children[2].addChild(Node(minusInfinity, [-19, -4, 12]))
    return root

def alphaBetaPruning(node, maxPlayer, depth,alpha, beta):
    children = node.children
    # base case
    if depth == 0 : #add node.is_terminal() condition
        # get values from heursitic function
        values = node.values
        for value in values:
            if alpha > beta:
                print("Pruning")
                break
            if maxPlayer:
                if value > node.value:
                    node.value = value
                    path.insert(depth, {node: node.value})
                alpha = max(alpha, value)
            else:
                if value < node.value:
                    node.value = value
                    path.insert(depth, {node: node.value})
                beta = max(beta, value)
        return node.value
    for child in children:
        value = alphaBetaPruning(child, not maxPlayer, depth-1,alpha, beta)
        if maxPlayer:
            alpha = max(alpha, value)
            if value > node.value:
                node.value = value
                path.insert(depth, {node: node.value})
            # node.value = max(node.value, value)
        else:
            beta = min(beta, value)
            if value < node.value:
                node.value = value
                path.insert(depth, {node: node.value})
            #node.value = min(node.value, value)
    return node.value


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = createTree()
    print(alphaBetaPruning(root, True, 2,minusInfinity, infinity))
    for i in range(3):
         for node in path[i].keys():
             print(f"Node: {node.random}, value: {path[i].values()}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
