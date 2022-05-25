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

from game import Directions, Grid
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

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
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


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first. 

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    dfs_node_sequence=util.Stack()#LIFO is used for depth first search 
    path_to_state={}#for each state we have visited, we will keep a path that allows us to go there, so that in each action the path to the child node is derived from the path to the parent's node in addition to the action taken to get to the child 
    visited_nodes=set()#better time complexity
    dfs_node_sequence.push(problem.getStartState())
    path_to_state[problem.getStartState()]=[]#empty list for Start State

    while (not dfs_node_sequence.isEmpty()):#mostly standart DFS code
        node_state=dfs_node_sequence.pop()
        if problem.isGoalState(node_state):
            return path_to_state[node_state]
        if node_state not in visited_nodes:
            visited_nodes.add(node_state)
            possbile_moves=problem.expand(node_state)
            for (child_state,action,_) in possbile_moves:
                #if (child_state not in path_to_state.keys()):
                path_to_state[child_state]=path_to_state[node_state]+[action]#we add the two lists, and now we have the path to each child of the parent node
                dfs_node_sequence.push(child_state)

    return None

def breadthFirstSearch(problem):#similar to dfs with a few changes

    bfs_node_sequence=util.Queue()#FIFO is used for breadth first search 
    path_to_state={}
    visited_nodes=set()
    bfs_node_sequence.push(problem.getStartState())
    path_to_state[problem.getStartState()]=[]

    while (not bfs_node_sequence.isEmpty()):
        node_state=bfs_node_sequence.pop()
        if problem.isGoalState(node_state):
            return path_to_state[node_state]
        if node_state not in visited_nodes:
            visited_nodes.add(node_state)
            possbile_moves=problem.expand(node_state)
            for (child_state,action,_) in possbile_moves:
                if (child_state not in path_to_state.keys()):#in contrast to dfs, we want a path to be derived only from the first parent to ever access it
                    path_to_state[child_state]=path_to_state[node_state]+[action]#(meaning that if C has parents A(closer to root) and B(further from root), then it's path should be calculated from the node that is closer to the Start State i.e A)
                    bfs_node_sequence.push(child_state)#for the correctness of the expanded nodes in autograder, we do not check whether a child is a goal state  

    return None

def nullHeuristic(state, problem=None):
    
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    A_star_queue=util.PriorityQueue()
    path_to_state={}
    visited_nodes=set()

    A_star_queue.push(problem.getStartState(),heuristic(problem.getStartState(),problem))#the priority of the Start State doesn't really matter as it is the only item in the queue

    path_to_state[problem.getStartState()]=[0,[]]#[0] is cost to got to child, and [1] is path that gives us said cost 

    while (not A_star_queue.isEmpty()):
        node_state=A_star_queue.pop()
        if problem.isGoalState(node_state):
            return path_to_state[node_state][1]
        if node_state not in visited_nodes:
            visited_nodes.add(node_state)
            possbile_moves=problem.expand(node_state)
            for (child_state,action,_) in possbile_moves:
                if (child_state in path_to_state.keys()):#if child has already been expanded, then we check if there is a need to update the path to it
                    if (path_to_state[child_state][0]>problem.getActionCost(node_state,action,child_state)+path_to_state[node_state][0]):
                        path_to_state[child_state]=[path_to_state[node_state][0]+problem.getActionCost(node_state,action,child_state),path_to_state[node_state][1]+[action]]
                        A_star_queue.update(child_state,path_to_state[child_state][0])
                else:
                    path_to_state[child_state]=[path_to_state[node_state][0]+problem.getActionCost(node_state,action,child_state),path_to_state[node_state][1]+[action]]
                    A_star_queue.push(child_state,heuristic(child_state,problem)+path_to_state[child_state][0])


    
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch

          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
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


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first. 

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    dfs_node_sequence=util.Stack()#LIFO is used for depth first search 
    path_to_state={}#for each state we have visited, we will keep a path that allows us to go there, so that in each action the path to the child node is derived from the path to the parent's node in addition to the action taken to get to the child 
    visited_nodes=[]
    dfs_node_sequence.push(problem.getStartState())
    path_to_state[problem.getStartState()]=[]#empty list for Start State

    while (not dfs_node_sequence.isEmpty()):#mostly standart DFS code
        node_state=dfs_node_sequence.pop()
        if problem.isGoalState(node_state):
            return path_to_state[node_state]
        if node_state not in visited_nodes:
            visited_nodes.append(node_state)
            possbile_moves=problem.expand(node_state)
            for (child_state,action,_) in possbile_moves:
                #if (child_state not in path_to_state.keys()):
                path_to_state[child_state]=path_to_state[node_state]+[action]#we add the two lists, and now we have the path to each child of the parent node
                dfs_node_sequence.push(child_state)

    return None

def breadthFirstSearch(problem):#similar to dfs with a few changes

    bfs_node_sequence=util.Queue()#FIFO is used for breadth first search 
    path_to_state={}
    visited_nodes=[]
    bfs_node_sequence.push(problem.getStartState())
    path_to_state[problem.getStartState()]=[]

    while (not bfs_node_sequence.isEmpty()):
        node_state=bfs_node_sequence.pop()
        if problem.isGoalState(node_state):
            return path_to_state[node_state]
        if node_state not in visited_nodes:
            visited_nodes.append(node_state)
            possbile_moves=problem.expand(node_state)
            for (child_state,action,_) in possbile_moves:
                if (child_state not in path_to_state.keys()):#in contrast to dfs, we want a path to be derived only from the first parent to ever access it
                    path_to_state[child_state]=path_to_state[node_state]+[action]#(meaning that if C has parents A(closer to root) and B(further from root), then it's path should be calculated from the node that is closer to the Start State i.e A)
                    bfs_node_sequence.push(child_state)

    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    A_star_queue=util.PriorityQueue()
    path_to_state={}
    visited_nodes=set()

    A_star_queue.push(problem.getStartState(),heuristic(problem.getStartState(),problem))

    path_to_state[problem.getStartState()]=[0,[]]

    while (not A_star_queue.isEmpty()):
        node_state=A_star_queue.pop()
        if problem.isGoalState(node_state):
            return path_to_state[node_state][1]
        if node_state not in visited_nodes:
            visited_nodes.add(node_state)
            possbile_moves=problem.expand(node_state)
            for (child_state,action,_) in possbile_moves:
                #if (child_state not in path_to_state.keys()):#in contrast to dfs, we want a path to be derived only from the first parent to ever access it
                if (child_state in path_to_state.keys()):
                    if (path_to_state[child_state][0]>problem.getActionCost(node_state,action,child_state)+path_to_state[node_state][0]):
                        path_to_state[child_state]=[path_to_state[node_state][0]+problem.getActionCost(node_state,action,child_state),path_to_state[node_state][1]+[action]]
                        A_star_queue.update(child_state,path_to_state[child_state][0])
                else:
                    path_to_state[child_state]=[path_to_state[node_state][0]+problem.getActionCost(node_state,action,child_state),path_to_state[node_state][1]+[action]]
                    A_star_queue.push(child_state,heuristic(child_state,problem)+path_to_state[child_state][0])


    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch