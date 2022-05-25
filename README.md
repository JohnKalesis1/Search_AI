# Search_AI
Implementing and utilizing search algorithms for use in the Pacman game and solving a Constrain Satisfaction Problem


In search.py I have implemented the BreadthFirstSearch, DepthFirstSearch and A* Search algorithms.

In SearchAgents.py I have created two heuristics for use in the A*(both consistend and admissable), 
one that allows for getting the minimun path to traverse the four corners of the maze, 
and one that allows for traversing the minimum path to eat all foods in the maze.(no ghosts exist in the two previous cases)

In multiagents.py I implement the MinMax, AlphaBeta and Expectimax algorithms(a limited depth option being allowed),
which are used in order to create a Pacman Agent which can beat mazes where one ghost is present.
(Part of this included creating an extensive evaluation function which allows us for taking a decision by only checking a couply of steps ahead(3-4 steps) in the decision trees
(In cases of 2 or more ghosts, Pacman can still win, but sometimes falls into traps like entering a one way path and being blocked off in both sides by the ghosts)

In csp_curriculum_sove.py we solve the problem of organising a universities exam schedule with taking into account the constraints of:
->Classes of same professor cannot be in the same day
->Classes of the same semester cannot be in the same day
->Difficult classes must have a one day interval
->Labs must follow their repsective class examination.

In solving the csp, algorithms like MRV,FC,MAC are used.
