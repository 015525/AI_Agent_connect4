import pygame

width = 700
win = pygame.display.set_mode((width, width))
pygame.display.set_caption("Binary Tree")
BLACK = (0, 0, 0)
GREY = (150, 150, 150)

class Node():
    def __init__(self, x, y, radius, color, left, right):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.left = left
        self.right = right

    def get_location(self):
        return (self.x, self.y)
    def get_color(self):
        return self.color
    def get_radius(self):
        return self.radius
    def get_left(self):
        return self.left
    def get_right(self):
        return self.right
    def set_left(self, l):
        self.left = l
    def set_right(self, r):
        self.right = r
    def set_color(self, c):
        self.color = c
    def set_radius(self, r):
        self.radius = r
    def set_x(self, x):
        self.x = x
    def set_y(self, y):
        self.y = y

def create_node(width, levels):

    nodes = []
    finalTot = 2 ** (levels - 1)
    diamater = (width // finalTot) / 2
    radius = diamater // 2
    for lvl in range(levels):
        totlvl = 2 ** lvl
        start = (width // totlvl) / 2
        for node in range(totlvl):
            nodes.append(Node(start + ((width//totlvl)*node), (width//levels) * lvl + (width // levels / 2), radius, BLACK, None, None))
    for i in range(len(nodes)):
        if (2*i+1) < len(nodes) and nodes[2*i+1]:
            nodes[i].set_left(nodes[2*i+1])
        if (2 * i + 2) < len(nodes) and nodes[2 * i + 2]:
            nodes[i].set_right(nodes[2 * i + 2])
    return nodes
def draw_circles(win, width, levels, nodes):
    for node in nodes:
        pygame.draw.circle(win, node.get_color(), node.get_location(), node.get_radius())
def draw_lines(win, nodes):
    for node in nodes:
        if node.get_left() != None and node.get_right() != None:
            pygame.draw.line(win, BLACK, node.get_location(), node.get_left().get_location(), 2)
            pygame.draw.line(win, BLACK, node.get_location(), node.get_right().get_location(), 2)

def draw(win, width, levels, nodes):
    draw_lines(win, nodes)
    draw_circles(win, width, levels, nodes)
    pygame.display.update()
def main(win, width):
    pygame.init()
    win.fill(GREY)
    pygame.display.update()
    lvls = 4
    nodes = create_node(width, lvls)

    while True:
        draw(win, width, lvls, nodes)
main(win, width)
print("YES")