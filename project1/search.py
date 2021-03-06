# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class PathNode:
    def __init__(self, state, action=None, parent=None, cost=0):
        self.state = state
        self.action = action
        self.parent = parent
        self.cost = cost
    def getPath(self):
        node = self
        ret = [node.action]
        while node.parent:
            if node.parent.action:
                ret.append(node.parent.action)
            node = node.parent
        ret.reverse()
        return ret
    def __repr__(self):
        return self.state.__repr__()

def depthFirstSearch(problem):
    """
    Your DFS implementation goes here

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    frontier = util.Stack()
    frontier.push(PathNode(problem.getStartState()))
    visited = set()
    while not frontier.isEmpty():
        curNode = frontier.pop()
        if curNode.state in visited:
            continue
        # Check if nodes are goal states when we pop them off the frontier
        if problem.isGoalState(curNode.state):
            return curNode.getPath()
        visited.add(curNode.state)
        for (successor, action, _) in problem.getSuccessors(curNode.state):
            if successor not in visited:
                childNode = PathNode(successor, action, curNode)
                frontier.push(childNode)


def breadthFirstSearch(problem):
    """Your BFS implementation goes here. Like for DFS, your 
    search algorithm needs to return a list of actions that 
    reaches the goal.
    """
    # Check if the start state is the goal state, if so return an empty list
    startState = problem.getStartState()
    if problem.isGoalState(startState):
        return []
    frontier = util.Queue()
    frontier.push(PathNode(startState))
    visited = set()
    while not frontier.isEmpty():
        curNode = frontier.pop()
        if curNode.state in visited:
            continue
        visited.add(curNode.state)
        # print frontier.list
        for (successor, action, _) in problem.getSuccessors(curNode.state):
            if successor not in visited:
                childNode = PathNode(successor, action, curNode)
                # Check if nodes are goal states before adding them to the frontier
                if problem.isGoalState(childNode.state):
                    return childNode.getPath()
                frontier.push(childNode)

def uniformCostSearch(problem):
    """Your UCS implementation goes here. Like for DFS, your 
    search algorithm needs to return a list of actions that 
    reaches the goal.
    """
    frontier = util.PriorityQueue()
    frontier.push(PathNode(problem.getStartState()), 0)
    visited = set()
    while not frontier.isEmpty():
        curNode = frontier.pop()
        if curNode.state in visited:
            continue
        # Check if nodes are goal states when we pop them off the frontier
        if problem.isGoalState(curNode.state):
            return curNode.getPath()
        visited.add(curNode.state)
        for (successor, action, edgeCost) in problem.getSuccessors(curNode.state):
            if successor not in visited:
                frontier.push(PathNode(successor, action=action, parent=curNode, cost=curNode.cost+edgeCost), curNode.cost+edgeCost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Your A* implementation goes here. Like for DFS, your 
    search algorithm needs to return a list of actions that 
    reaches the goal. heueristic is a heuristic function - 
    you can see an example of the arguments and return type
    in "nullHeuristic", above.
    """
    frontier = util.PriorityQueue()
    frontier.push(PathNode(problem.getStartState()), heuristic(problem.getStartState(), problem))
    visited = set()
    while not frontier.isEmpty():
        curNode = frontier.pop()
        if curNode.state in visited:
            continue
        # Check if nodes are goal states when we pop them off the frontier
        if problem.isGoalState(curNode.state):
            return curNode.getPath()
        visited.add(curNode.state)
        for (successor, action, edgeCost) in problem.getSuccessors(curNode.state):
            if successor not in visited:
                g = curNode.cost + edgeCost
                h = heuristic(successor, problem)
                f = g + h
                frontier.push(PathNode(successor, action=action, parent=curNode, cost=g), f)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
