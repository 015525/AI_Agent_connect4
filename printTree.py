from treelib import *


nodes = []  # all nodes in the tree
tree = Tree()
tree.create_node(f"{nodes[0].state}", f"{nodes[0].state}")  # root node
for i in range(1, len(nodes)):
    for j in range(7 * i + 1, 7 * i + 8):
        if j < len(nodes):
            tree.create_node(f"{nodes[j].state}", f"{nodes[j].state}", parent=f"{nodes[i].state}")
        else:
            break
tree.show()

if __name__ == "__main__" :
    pass

