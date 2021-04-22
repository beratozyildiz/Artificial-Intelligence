"""
The code that finds the solution of E15 Puzzle. It generates 12 random input states and solves each of them.
The solutions of S1 and S2 is displayed in detail showing the necessary moves. The maximum queue size reached
is displayed for the remaining puzzles. The A* Search algorithm is implemented. The heuristic used is the number
of misplaced tiles. This is an admissible heuristic since all misplaced tiles should be moved at least once. 
The duplicate tiles do not pose a problem for admissiblity since the important thing is wheter a tile in current state matches
the tile in the goal state. The output confirms the admissiblity since the heuristic never overestimates the necessary moves.
"""
import state_generator
import graphing_tool
import matplotlib.pyplot as plt

class Node:
    """
    The class that represents a node and therefore, a state in a search problem.
    
    Attributes: 
        puzzle (list): puzzle as a 2d list or array
        hashable_puzzle (string): The state representation as a string that contains boxes from top left to rigth bottom
        action: action that is made to come to current state
        moving_tile (int): the tile that should be moved in order to come to this state
        children (list): the list of possible states that can be moved to
        parent(string): the string state representation of parent state
        empty_tile (tuple): the position of empty tile
        heuristic (int): heuristic value for the current state
        cost (int): Number of steps taken to come from initial state to current state
        total_expense (int): cost + heuristic value
    """  
    def __init__(self, puzzle , action = None, moving_tile = None):

        self.puzzle = puzzle
        self.hashable_puzzle = self.hash_puzzle()
        self.action = action
        self.moving_tile = moving_tile
        self.parent = None
        self.children = []
        self.empty_tile = self.find_empty_tile_()
        self.heuristic = self.calculate_heuristic()
        self.cost = 0
        self.total_expense = self.cost + self.heuristic

    def add_child(self, state):
        self.children.append(state)

    def set_parent(self, state):
        self.parent = state

    def calculate_heuristic(self):
        """
        Calculates the heuristic for current state and returns the heuristic. The heuristic used is the 
        number of misplaced tiles. 
        Returns:
            misplaced_tiles (int): number of misplaced tiles
        """
        places = { (0,0) : 1,
                    (0,1) : 2,
                    (0,2) : 3,
                    (0,3) : 4,
                    (1,0) : 2,
                    (1,1) : 3,
                    (1,2) : 4,
                    (1,3) : 5,
                    (2,0) : 3,
                    (2,1) : 4,
                    (2,2) : 5,
                    (2,3) : 5,
                    (3, 0): 4,
                    (3, 1): 5,
                    (3, 2): 5,
                    (3, 3): 0}

        misplaced_tiles = 0

        for row in range(len(self.puzzle)):
            for column in range(len(self.puzzle[0])):
                if self.puzzle[row][column] != 0:
                    if self.puzzle[row][column] != places[(row,column)]:
                        misplaced_tiles += 1
        return misplaced_tiles

    def find_empty_tile_(self):
        """
        Iterates through the puzzle and returns the position of empty tile
        
        Returns:
            The tuple that contains the position of empty tile
        """
        for row in range(len(self.puzzle)):
            for column in range(len(self.puzzle[0])):
                if self.puzzle[row][column] == 0:
                    return (row, column)

    def clone_puzzle(self):
        """
        Clones the puzzle and returns the cloned puzzle
        
        Returns:
            puzzle_of_clone (list): the puzzle as 2d list
        """
        
        puzzle_of_clone = []
        for row in self.puzzle:
            puzzle_of_clone.append([col for col in row])
        return puzzle_of_clone


    def move(self,action):
        """
        Moves the empty tile in the specified direction and returns both the new state and 
        the tile that should be moved physically
        
        Args:
            action (string): The direction that empty tile will move to
        Returns:
            clone (list): New state as a 2d list
            tile_to_go (int): Tile that should be moved physically to perform the operation
        """
        actions = {"u" : (-1,0),
                    "d" : (1,0),
                    "l" : (0,-1),
                    "r" : (0,1)
                    }
        clone = self.clone_puzzle()
        tile_to_go = clone[self.empty_tile[0]+actions[action][0]][self.empty_tile[1]+actions[action][1]]
        clone[self.empty_tile[0]][self.empty_tile[1]] = tile_to_go
        clone[self.empty_tile[0] + actions[action][0]][self.empty_tile[1] + actions[action][1]] = 0
        return clone,tile_to_go


    def hash_puzzle(self):
        """
        Returns a string representation of current state.
        
        Returns:
            hashable_puzzle (string): the current puzzle state that is converted to string
        """
        hashable_puzzle = ""
        for row in self.puzzle:
            for col in row:
                hashable_puzzle += str(col)
        return hashable_puzzle


class QueueLine():
    """   
    The class that realizes the queue in a search problem. The states are removed from
    the front of the queue and the sorting is made outside during the search
    
    Attributes:
        queue (list): holds the states to realize the queue
        max (int): maximum number of elements in the queue at any time
    """
    def __init__(self):
        self.queue = []
        self.max = 0

    def add(self, neighbour):
        self.queue.append(neighbour)
        if (len(self.queue) > self.max):
            self.max = len(self.queue)
    def empty(self):
        if len(self.queue) == 0:
            return True

    def remove(self):
        #check if queue is empty
        if self.empty():
            raise Exception("queue is empty")
        else:
            #take the first element in the queue
            state = self.queue[0]
            #update the queue by eliminating the first element
            self.queue = self.queue[1:]
            return state          


class Space:
    """
    The class that realizes the notion of search space. It applies the A* search algorithm to solve
    the E15 puzzle.
    
    Attributes:
        start_node (Node): the initial state node
        nodes (dict): the dictionary that holds the states in the search space
        start (string): the start state representation (assumes everyone is in the west side)
        goal(string): the goal state representation (assumes the goal is to have everyone in the east side)
    """
    def __init__(self, start_node):
        self.start_node = start_node
        self.nodes={}
        self.start = self.start_node.hashable_puzzle
        self.nodes[self.start] = start_node
        self.goal = "1234234534554550"


    def add_node(self,node):
        self.nodes[node.hashable_puzzle] = node

    def generate_possible_moves(self,state):
        """
        Generates the possible moves for the current state and updates the nodes dictionary
        
        Args:
            state (string): string representation of the current state
        """
        #check if the empty tile is at the top row
        if self.nodes[state].empty_tile[0] != 0:
            new_puzzle,moving_tile = self.nodes[state].move("u")
            child = Node(puzzle = new_puzzle, action="u",moving_tile=moving_tile)
            if child.hashable_puzzle not in self.nodes.keys():
                self.add_node(child)
            self.nodes[state].add_child(child.hashable_puzzle)
        #check if the empty tile is at the bottom row
        if self.nodes[state].empty_tile[0] != 3:
            new_puzzle,moving_tile = self.nodes[state].move("d")
            child = Node(puzzle=new_puzzle, action="d",moving_tile=moving_tile)
            if child.hashable_puzzle not in self.nodes.keys():
                self.add_node(child)
            self.nodes[state].add_child(child.hashable_puzzle)
        #check if the empty tile is at the left-most column
        if self.nodes[state].empty_tile[1] != 0:
            new_puzzle,moving_tile = self.nodes[state].move("l")
            child = Node(puzzle=new_puzzle, action="l",moving_tile=moving_tile)
            if child.hashable_puzzle not in self.nodes.keys():
                self.add_node(child)
            self.nodes[state].add_child(child.hashable_puzzle)
        #check if the empty tile is at the right-most column
        if self.nodes[state].empty_tile[1] != 3:
            new_puzzle, moving_tile = self.nodes[state].move("r")
            child = Node(puzzle=new_puzzle, action="r",moving_tile=moving_tile)
            if child.hashable_puzzle not in self.nodes.keys():
                self.add_node(child)
            self.nodes[state].add_child(child.hashable_puzzle)
    def get_total_expense(self,state):
        return self.nodes[state].total_expense
    
    def solve(self):
        """
        The method that tries to find the goal state and a path from start state to goal state, if it exists. Initially
        the search space only includes the start state and it is expanded as the search goes on. The A* search algorithm
        is used for the search
        """
        Queue = QueueLine()
        Queue.add(self.start)
        self.visited = []
        i = 0
        while True:
            current_state = Queue.remove()
            i += 1
            #check if the current state is the goal state
            if current_state == self.goal:
                solution = []
                max_elements.append(Queue.max)
                self.visited.append(current_state)
                #Trace back to find the path
                while self.nodes[current_state].parent:
                    solution.append(current_state)
                    current_state = self.nodes[current_state].parent

                solution.append(self.start)
                solution.reverse()
                print("Length of solution:", len(solution))
                print("Number of visited states:", i)
                return solution

            self.visited.append(current_state)
            #generate possible moves from the current state
            self.generate_possible_moves(current_state)
            #iterate through the neighbours of current state
            for neighbour in self.nodes[current_state].children:
                #if child is not in queue and not visited than add it to queue and update the cost
                if neighbour not in Queue.queue and neighbour not in self.visited:
                    self.nodes[neighbour].set_parent(current_state)
                    self.nodes[neighbour].cost = self.nodes[current_state].cost + 1
                    self.nodes[neighbour].total_expense =  self.nodes[neighbour].cost +  self.nodes[neighbour].heuristic
                    Queue.add(neighbour)
                    #sort the key with total expense values (cost + heuristic)
                    Queue.queue.sort(key = self.get_total_expense)
                #if there is a shorter path to a node already in the queue, replace it with the shorter one (dynamic programming)
                elif neighbour in Queue.queue and neighbour not in self.visited:
                    if (self.nodes[current_state].cost <self.nodes[self.nodes[neighbour].parent].cost):
                        self.nodes[neighbour].set_parent(current_state)
                        self.nodes[neighbour].cost = self.nodes[current_state].cost + 1
                        self.nodes[neighbour].total_expense = self.nodes[neighbour].cost + self.nodes[
                            neighbour].heuristic
                        Queue.queue.sort(key=self.get_total_expense)
def print_puzzle(puzzles):
    """
    Prints the generated initial puzzles
    
    Args:
        puzzles (dict): The dictionary that holds the initial states of 12 distinct puzzles
    """
    for el in puzzles:
        print("**********"+el+"**********")
        for row in puzzles[el]:
            print(row)
def find_moves(actions,tiles):
    """
    Finds the list of moves that should be done physically
    
    Args:
        actions (list): actions of empty tiles to go from initial state to goal state
        tiles (list): tiles that should be moved in the order (the same indexing with actions)
    Returns:
        moves (list): the list of moves
    """
    moves = []
    #actions list holds the actions for empty tile, the real moves are the reverse move of that action
    for i in range(len(actions)):
        if actions[i] == "u":
            moves.append("{} down".format(tiles[i]))
        elif actions[i] == "d":
            moves.append("{} up".format(tiles[i]))
        elif actions[i] == "l":
            moves.append("{} right".format(tiles[i]))
        elif actions[i] == "r":
            moves.append("{} left".format(tiles[i]))
    return moves
def convert_to_list(solution):
    """
    Converts solution represented as stirng to a list and returns that list  
        Args:
            solution (string): string representation of solution
        Returns:
            solution_list (list): The 1D list holding the numbers from left to right and from top to down in the order.
    """
    solution_list = []
    for el in solution:
        state = []
        for ch in el:
            state.append(int(ch))
        solution_list.append(state)
    return solution_list


plt.clf()
max_elements = []
inputs = state_generator.generate_states()
j = 1
puzzles = {}
#Name the states and hold in dictionary
for state in inputs:
    puzzles["S{}".format(j)] = state
    j += 1
print_puzzle(puzzles)
#create dictionaries to hold the solution paths and moves of all puzzle problems
solution_paths = {}
solution_moves = {}
#iterate through the initial puzzle problems to solve them
for puzzle in puzzles.keys():
    print("\nSolution for {}".format(puzzle))
    #create the node for initial state
    y = Node(puzzle = puzzles[puzzle], action = None)
    #create the search space
    s = Space(y)
    #solve the puzzle
    solution = s.solve()

    print( "Solution path with string representations of states")
    print(solution)
    print("Cost values of solution path nodes from start to goal: ")
    c = [s.nodes[x].cost for x in solution]
    print(c)
    print("Heuristic values of solution path nodes from start to goal: ")
    h = [s.nodes[x].heuristic for x in solution]
    print(h)
    print("Total expense of solution path nodes from start to goal: ") #Total expense never decreases from start to goal, which shows the admissibility of heuristic
    t = [s.nodes[x].total_expense for x in solution]
    print(t)

    #get actions and tiles in the order from start to goal
    actions = [s.nodes[x].action for x in solution]
    tiles = [s.nodes[x].moving_tile for x in solution]
    
    #find moves that should be made physically (empty tile cannot move in real problem) 
    moves = find_moves(actions,tiles)
    output = convert_to_list(solution)
    #hold the solution paths and moves
    solution_paths[puzzle] = output
    solution_moves[puzzle] = moves
    
#pick the first two puzzle to show each step graphically and take paths and moves
solutions_to_graph = [solution_paths["S1"],solution_paths["S2"]]
moves_to_graph = [solution_moves["S1"],solution_moves["S2"]]
#find the x and y axis values of state vs max queue size graph
remaining_states = list(puzzles.keys())[2:12]
max_for_remaining = max_elements[2:12]
#create new thread to display the puzzle graphics
thread1 = graphing_tool.new_thread(1, "Thread-1", solutions_to_graph, moves_to_graph)
thread1.start()
#plot the state vs max queue size graph
plt.bar(remaining_states, max_for_remaining)
plt.title("State Names vs Max Queue Size")
plt.show()




