# multiAgents.py
# --------------
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


from signal import setitimer
from time import clock_settime, sleep
from pacman import GameState
from pacmanAgents import scoreEvaluation
from util import manhattanDistance
from game import Directions, Game
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        LIMIT=99999
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        oldPos=currentGameState.getPacmanPosition()
        if (oldPos==newPos):
            return -1
        if (currentGameState.hasFood(newPos[0],newPos[1]) and (newPos not in childGameState.getGhostPositions())):
            return 2        
        highest_threat=LIMIT
        for ghost in newGhostStates:
            ghost_dist_to_pacman=manhattanDistance(newPos,ghost.configuration.getPosition())
            if (ghost_dist_to_pacman<highest_threat):
                highest_threat=ghost_dist_to_pacman
        foodlist=newFood.asList()
        if (highest_threat==0):
            return -2
        if (highest_threat<=2): 
            return -1/highest_threat
        closest_dot=LIMIT
        for food in foodlist:
            pacman_dist_to_food=util.manhattanDistance(food,newPos)
            if (pacman_dist_to_food<closest_dot):
                closest_dot=pacman_dist_to_food
        return 1/closest_dot


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def MAX(self,GameState,depth):
        max=-999999
        best_action=None
        if (GameState.isLose() or GameState.isWin() or self.depth==depth):
            return self.evaluationFunction(GameState)
        for action in GameState.getLegalActions(0):
            childGameState=GameState.getNextState(0,action)  
            score=self.MIN(childGameState,depth,1)
            if (score>max):
                max=score
                best_action=action
        if (depth==0):
            return best_action
        else: 
            return max


    def MIN(self,GameState,depth,layer):
        min=999999
        if (GameState.isLose() or GameState.isWin()):
            return self.evaluationFunction(GameState)
        else:
            for action in GameState.getLegalActions(layer):
                childGameState=GameState.getNextState(layer,action)
                if (layer==(childGameState.getNumAgents()-1)):
                    score=self.MAX(childGameState,depth+1)
                else:   
                    score=self.MIN(childGameState,depth,layer+1)
                if (score<min):
                    min=score
            return min

            
    def Minimax(self,GameState):
        best_acion=self.MAX(GameState,0)
        return best_acion


    def getAction(self, gameState):
        return self.Minimax(gameState)
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def Max_value(self,GameState,depth,a,b):
        max=-999999
        best_action=None
        if (GameState.isLose() or GameState.isWin() or self.depth==depth):
            return self.evaluationFunction(GameState)
        for action in GameState.getLegalActions(0):
            childGameState=GameState.getNextState(0,action)  
            score=self.Min_value(childGameState,depth,1,a,b)
            if (score>max):
                max=score
                best_action=action
            if (max>b):
                return max 
            if (a<max):
                a=max
        if (depth==0):
            return best_action
        else: 
            return max

    def Min_value(self,GameState,depth,layer,a,b):
        min=999999
        if (GameState.isLose() or GameState.isWin()):
            return self.evaluationFunction(GameState)
        else:
            for action in GameState.getLegalActions(layer):
                childGameState=GameState.getNextState(layer,action)
                if (layer==(childGameState.getNumAgents()-1)):
                    score=self.Max_value(childGameState,depth+1,a,b)
                else:   
                    score=self.Min_value(childGameState,depth,layer+1,a,b)
                if (score<min):
                    min=score
                #if (layer==(childGameState.getNumAgents()-1)):
                if (min<a):
                    return min
                if (min<b):
                    b=min
            return min

    def alpha_beta(self,gameState):
        a=-99999
        b=99999
        return  self.Max_value(gameState,0,a,b)

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.alpha_beta(gameState)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def Max_Value(self,GameState,depth):
        max=-999999
        best_action=None
        if (GameState.isLose() or GameState.isWin() or self.depth==depth):
            return self.evaluationFunction(GameState)
        for action in GameState.getLegalActions(0):
            childGameState=GameState.getNextState(0,action)  
            score=self.Expected_value(childGameState,depth,1)
            if (score>max):
                max=score
                best_action=action
        if (depth==0):
            return best_action
        else: 
            return max

    def Expected_value(self,GameState,depth,layer):
        if (GameState.isLose() or GameState.isWin()):
            return self.evaluationFunction(GameState)
        else:
            sum=0
            for action in GameState.getLegalActions(layer):
                childGameState=GameState.getNextState(layer,action)
                if (layer==(childGameState.getNumAgents()-1)):
                    score=self.Max_Value(childGameState,depth+1)
                else:   
                    score=self.Expected_value(childGameState,depth,layer+1)
                sum=sum+score
            return sum/len(GameState.getLegalActions(layer))
    def excpectimax(self,GameState):
        #self.evaluationFunction=betterEvaluationFunction
        #self.depth=2
        probably_best_action=self.Max_Value(GameState,0)
        return probably_best_action
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.excpectimax(gameState)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    LIMIT=99999
    
    pacman_pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    foodlist=Food.asList()

    Score=currentGameState.getScore()
    if (currentGameState.isWin()):
        return Score
    if (currentGameState.isLose()):
        return Score
    for ghost in GhostStates:
        ghost_pos=ghost.configuration.getPosition()
        kill_dist=manhattanDistance(pacman_pos,ghost_pos)
        if (ghost.scaredTimer>0 and kill_dist<(ghost.scaredTimer+1)):
            Score+=100/kill_dist
    closest_dot=[LIMIT,None]
    for food in foodlist:
        pacman_dist_to_food=manhattanDistance(food,pacman_pos)
        if (pacman_dist_to_food<closest_dot[0]):
            closest_dot[0]=pacman_dist_to_food
            closest_dot[1]=food
    Score+=1/(closest_dot[0])+0.0001*(visbility(pacman_pos,closest_dot[1],currentGameState))
    closest_capsule=[LIMIT,None]
    for capsule in currentGameState.getCapsules():
        pacman_dist_to_capsule=manhattanDistance(pacman_pos,capsule)
        if (pacman_dist_to_capsule<closest_capsule[0]):
            closest_capsule[0]=pacman_dist_to_capsule
            closest_capsule[1]=capsule
    closest_victim=[LIMIT,None]
    
    if (closest_capsule[1]!=None):
        for ghost in GhostStates:
            ghost_pos=manhattanDistance(ghost.configuration.getPosition(),closest_capsule[1])
            if (ghost_pos<closest_victim[0]):
                closest_victim[0]=ghost_pos
                closest_victim[1]=ghost
        Score+=20/closest_capsule[0]+0.00001*visbility(pacman_pos,closest_capsule[1],currentGameState)
    return Score
        
# Abbreviation
better = betterEvaluationFunction

def visbility(pos,goal,currentGameState):
    vertical_visibility=0
    horizontal_visibility=0
    if ((goal[1]-pos[1])>0):#look up
        i=1
        while (goal[1]-(pos[1]+i))>0:
            if (currentGameState.hasWall(pos[0],pos[1]+i)):
                break
            i+=1
        horizontal_visibility=i
    if ((pos[1]-goal[1])>0):#look down
        i=1
        while ((pos[1]-(goal[1]+i))>0):
            if (currentGameState.hasWall(pos[0],pos[1]-i)):
                break
            i+=1
        horizontal_visibility=i
    if ((goal[0]-pos[0])>0):#look right
        i=1
        while (goal[0]-(pos[0]+i))>0:
            if (currentGameState.hasWall(pos[0]+i,pos[1])):
                break
            i+=1
        vertical_visibility=i
    if ((pos[0]-goal[0])>0):#look left
        i=1
        while ((pos[0]-(goal[0]+i))>0):
            if (currentGameState.hasWall(pos[0]-i,pos[1])):
                break
            i+=1
        vertical_visibility=i
    return vertical_visibility+horizontal_visibility

