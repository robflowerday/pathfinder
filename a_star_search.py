import grids
from collections import deque

class State:
    def __init__(self, locationIn, gridIn, hamming_distanceIn):
        self.number = gridIn[locationIn[0]][locationIn[1]]
        self.location = locationIn
        self.id = locationIn[0] * len(gridIn[0]) + locationIn[1]
        self.hamming_distance = hamming_distanceIn
        
class Node:
    def __init__(self, stateIn, depthIn, parentIn=None, operatorIn=None, path_costIn=None):
        self.state = stateIn
        self.parent = parentIn
        self.operator = operatorIn
        self.depth = depthIn
        self.path_cost = path_costIn

def find_goal_location(gridIn):
    for x in range(len(gridIn)):
        for y in range(len(gridIn[0])):
            if gridIn[x][y] == 3:
                return [x, y]

def determine_hamming_distance(locationIn, gridIn):
    goal_location = find_goal_location(gridIn)
    goalX = goal_location[0]
    goalY = goal_location[1]
    locX = locationIn[0]
    locY = locationIn[1]
    difX = abs(goalX - locX)
    difY = abs(goalY - locY)
    return difX + difY

def create_initial_node(gridIn):
    for x in range(len(gridIn)):
        for y in range(len(gridIn[0])):
            if gridIn[x][y] == 2:
                return Node(State([x, y], gridIn, determine_hamming_distance([x, y], gridIn)), depthIn=0)

def valid_location(locationIn, gridIn, visitedIn):
    x = locationIn[0]
    y = locationIn[1]
    if (x >= 0) and (x < len(gridIn)) and (y >= 0) and (y < len(gridIn[0]) and (gridIn[x][y] != 1) and (locationIn not in visitedIn)):
        return True
    return False

def right_node(nodeIn, gridIn, visitedIn):
    x = nodeIn.state.location[0]
    y = nodeIn.state.location[1] + 1
    location = [x,y]
    if valid_location(location, gridIn, visitedIn):
        return Node(State(location, gridIn, determine_hamming_distance([x, y], gridIn)), nodeIn.depth + 1, parentIn=nodeIn, operatorIn="right")

def left_node(nodeIn, gridIn, visitedIn):
    x = nodeIn.state.location[0]
    y = nodeIn.state.location[1] - 1
    location = [x,y]
    if valid_location(location, gridIn, visitedIn):
        return Node(State(location, gridIn, determine_hamming_distance([x, y], gridIn)), nodeIn.depth + 1, parentIn=nodeIn, operatorIn="left")

def up_node(nodeIn, gridIn, visitedIn):
    x = nodeIn.state.location[0] + 1
    y = nodeIn.state.location[1]
    location = [x,y]
    if valid_location(location, gridIn, visitedIn):
        return Node(State(location, gridIn, determine_hamming_distance([x, y], gridIn)), nodeIn.depth + 1, parentIn=nodeIn, operatorIn="up")

def down_node(nodeIn, gridIn, visitedIn):
    x = nodeIn.state.location[0] - 1
    y = nodeIn.state.location[1]
    location = [x,y]
    if valid_location(location, gridIn, visitedIn):
        return Node(State(location, gridIn, determine_hamming_distance([x, y], gridIn)), nodeIn.depth + 1, parentIn=nodeIn, operatorIn="down")

def expand_node(nodeIn, gridIn, stackIn, visitedIn):
    
    node1 = right_node(nodeIn, gridIn, visitedIn)
    node2 = left_node(nodeIn, gridIn, visitedIn)
    node3 = up_node(nodeIn, gridIn, visitedIn)
    node4 = down_node(nodeIn, gridIn, visitedIn)
    nodes = [node1, node2, node3, node4]

    for node in nodes:
        if node:
            stackIn.append(node)
            visitedIn.append(node.state.location)

def goal_test(nodeIn):
    if nodeIn.state.number == 3:
        return True
    return False

def make_stack(nodesIn):
    stack = []
    for node in nodesIn:
        stack.append(node)
    return stack

def a_srtar_search(gridIn):

    initial_node = create_initial_node(gridIn)
    frontier = make_stack([initial_node])
    visited = []

    x = 0
    while True:
        x += 1
        try:
            frontier.sort(reverse=True, key=lambda x: x.state.hamming_distance + x.depth)
            visited = []
            for node in frontier:
                visited.append(node.state.location)
            node = frontier.pop()

        except IndexError:
            print(f"Search has failed")
            return False
        else:
            if goal_test(node):
                return node
            expand_node(node, gridIn, frontier, visited)
    



def displayIDSResult(gridIn):
    result = a_srtar_search(gridIn)
    print("solution found")
    print(result.state.location)
    while result.parent:
        print(result.parent.state.location)
        result = result.parent

displayIDSResult(grids.grid5)