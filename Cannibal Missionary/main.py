"""
The code that tries to solve the cannibals and missionaries problem. All the cannibals and missionaries
are assumed to be on the west side and the aim is to take everyone to the east side safely. The code is 
designed for the problems that the number of cannibals or missionaries doesn't exceed 9. The program uses
the Breadth-First Search (BFS) algorithm to find the path from the start state to goal state. For the second 
question part a is attempted.
"""
class Node():
    """
    The class that represents a node and therefore, a state in a search problem. Each node has a state, a list of childs
    and a parent.
    
    Attributes: 
        state (string): state representation consisting of three numbers in the order "cannibals on
            west,missionaries on west, boat position(0 for west, 1 for east)"
        child (list): the list of safe states that can be moved to from this state safely
        parent(string): the state that we came from during the search (none for start state)
    """  
    def __init__(self, state):
        self.state = state  # state representation as a string        
        self.child = []     #child list which will hold state names that can be moved to from this node
        self.parent = None

    def set_parent(self, parent):
        """
        Sets the parent of the node
        
        Args:
            parent (string): the state that we added the current state to the queue as a child of
        """
        self.parent = parent

    def add_child(self, child):
        """
        Adds a new safe state that can be moved to safely, to the child list

        Args:
            child (string): a safe state that can be moved to safely 
        """ 
        self.child.append(child)

class QueueLine():
    """
    The class that realizes the queue in a search problem. Breadth-First Search (BFS)
    logic is used in the operation of queue. The elements are added to the back of the queue 
    and removed from the front of the queue when it is required.
    
    Attributes:
        queue (list): holds the states to realize the BFS algorithm 
    """
    def __init__(self):
        self.queue = []

    def add(self, neighbour):
        """
        Adds the neighbour or child state to back of the queue
        
        Args:
            neighbour (string): state that will be added to queue
        """
        self.queue.append(neighbour)

    def remove(self):
        """
        Removes and returns the state from the front of the queue (BFS logic)
        
        Returns:
            state(string): The state in the front of the queue
        
        Raises:
            Exception: if the queue is empty
        """
        #check if queue is empty
        if len(self.queue) == 0:
            raise Exception("queue is empty")
        else:
            #take the last element in the queue
            state = self.queue[0]
            #update the queue by eliminating the last element
            self.queue = self.queue[1:]
            return state


class Space():
    """
    The class that realizes the notion of search space. It includes the tools to 
    solve the cannibals-missonaries problem. The main program, only interacts with or 
    uses this class.
    
    Attributes:
        cannibals (int): number of cannibals in the problem
        missonaries (int): number of missonaries in the problem
        boat_size (int): the maximum number of people a boat can carry
        nodes (dict): the dictionary that holds the states in the search space
        start (string): the start state representation (assumes everyone is in the west side)
        goal(string): the goal state representation (assumes the goal is to have everyone in the east side)
    """
    def __init__(self, cannibals, missionaries, boat_size):
        self.cannibals = cannibals  #total number of cannibals in the problem
        self.missionaries = missionaries  #total numbers of missionaries in the problem
        self.boat_size = boat_size  #boat size in the problem
        self.nodes = {}   #dictionary that will hold the nodes in the search space
        # create the string representation of start state to refer in nodes dictioanary
        self.start = "{}{}{}".format(cannibals, missionaries, 0)
        node = Node(self.start)
        self.__add_node__(node)
        # set the parent of start state as None
        self.nodes[self.start].set_parent(None)
        # create the string representation of goal state
        self.goal = "{}{}{}".format(0, 0, 1)
        print("\nSearch space is created\n")
        
        
    def __add_node__(self, node):
        """
        Updates the nodes dictionary that holds the nodes in the search space

        Args:
            node (Node) : Node object that represent the state as a node
        """
        self.nodes[node.state] = node

                                    
    def __is_safe__(self, west_c, west_m):
        """
        Takes the state variables (cannibals on west, missionaris on west) and returns True 
        if the state is safe, False otherwise.

        Args:
            west_c (int): number of cannibals in the west side 
            west_m (int): number of missionaries in the west side

        Returns:
            True if a given state is safe for both sides, False otherwise
        """
        #find the numbers for east side
        east_c = self.cannibals - west_c
        east_m = self.missionaries - west_m
        #check if the numbers are greater than zero and less than maximum number
        if(west_c >= 0 and west_m >= 0 and east_c >= 0 and east_m >= 0 and west_c <= self.cannibals
           and west_m <= self.missionaries and east_c <= self.cannibals and east_m <= self.missionaries):
            #check if missionaries is in danger
            if(west_c <= west_m and east_c <= east_m or west_m == 0 or east_m == 0):
                return True
        return False
    
    def __generate_safe_transitions__(self,current_state):
        """
        Takes the current state as input and finds safe transitions to safe states and 
        add those safe states to child list of current state.

        Args:
            current_state (string): the current state from which we seek safe transitions to other safe states.
        """
        #generate all boat transitions
        for carried_cannibals in range(self.boat_size+1):
            for carried_missionaries in range(self.boat_size+1):
                #convert all state indicators to integer        
                west_c = int(current_state[0])
                west_m = int(current_state[1])
                boat_pos = int(current_state[2])
                #check if the total size is in boat size range
                if (carried_cannibals + carried_missionaries <= self.boat_size and carried_cannibals + carried_missionaries > 0):
                    #check if the situation in the boat is safe
                    if(carried_cannibals <= carried_missionaries or carried_missionaries == 0):
                        #detect the boat position
                        if (boat_pos == 0):
                            west_c = west_c - carried_cannibals
                            west_m = west_m - carried_missionaries
                            boat_pos = 1
                        elif (boat_pos == 1):
                            west_c = west_c + carried_cannibals
                            west_m = west_m + carried_missionaries
                            boat_pos = 0
                        #check if the next state is safe
                        if self.__is_safe__(west_c,west_m):                            
                            new_state = "{}{}{}".format(west_c,west_m,boat_pos)
                            #check if the node for new state is already created
                            if new_state not in self.nodes.keys():
                                #create the node for new state
                                node = Node(new_state)
                                #add the created node to search space
                                self.__add_node__(node)
                            #add new state to the child list of current state
                            self.nodes[current_state].add_child(new_state)
                                                
    def __give_output__(self,solution):
        """
        Takes the solution path as input and prints the solution in the desired form

        Args:
            solution (list): list that contains the path (the states that should be visitied 
                in order, to go from start state to goal state, including both end states)
        """
        previous_state = None
        #iterate over states to detect actions to be done
        for state in solution:
            #find the numbers of cannibals and missionaries for each side (west and east)
            west_c = int(state[0])
            east_c = self.cannibals - west_c
            west_m = int(state[1])
            east_m = self.missionaries - west_m
            
            #pass for the first cycle
            if (state != self.start):
                #detect the boat positon for previous state
                if (previous_state[2] == "0"):
                    #find the numbers of cannibals and missonaries to be sent to east
                    carried_c = int(previous_state[0]) - int(state[0])
                    carried_m = int(previous_state[1]) - int(state[1]) 
                    print("SEND {} Cannibals {} Missionaries".format(carried_c,carried_m))
                else:
                    #find the numbers of cannibals and missonaries to be returned to west
                    carried_c = int(state[0]) - int(previous_state[0])  
                    carried_m = int(state[1]) - int(previous_state[1])  
                    #print the action and the numbers in the boat
                    print("RETURN {} Cannibals {} Missionaries".format(carried_c,carried_m))                    
            #print the cannibals and missonaries for both side in two line
            print(west_c*'C', end = "\t\t\t\t\t")
            print(east_c*'C')
            print(west_m*'M', end = "\t\t\t\t\t")
            print(east_m*'M', end="\n\n")
            #assign current state to previous_state to find the next action for next transition
            previous_state = state
                       
    def solve(self):
        """
        The method that tries to find the goal state and a path from start state to goal state, if it exists. Initially
        the search space only includes the start state and it is expanded as the search goes by finding safe transitions
        and adding the child states.
        """
        #create queue object
        Queue = QueueLine()
        #add the start state to the queue
        Queue.add(self.start)
        print("Queue: {}\n".format(Queue.queue))
        #create an empty set for accounting visited states
        self.visited = []

        #loop until the solution is found or there is no more state in queue
        while True:
            #check if the queue is empty
            if len(Queue.queue) == 0:
                print("No solution")
                break
            #take the state from the queue
            state = Queue.remove()
            print("Check state: {}".format(state))

            #check if the state is goal state
            if state == self.goal:
                #create the solution list which will hold the path from start state to goal state
                solution = []
                self.visited.append(state)
                print("\n****Goal state found****\n")
                #backtrack upto the start state, whose parent is none, to find the path
                while self.nodes[state].parent is not None:
                    solution.append(state)
                    print("Parent of {} is {}".format(state,self.nodes[state].parent))
                    state = self.nodes[state].parent
                solution.append(self.start)
                #revert the list to be in the order from start to goal
                solution.reverse()
                
                print("\n****Path as a list****\n")
                print(solution)
                
                print("\n****Actions to be done****\n")
                #print the actions to be done in desired form
                self.__give_output__(solution)
                break

            #add the state to visited list
            self.visited.append(state)
            
            #find the states that can be moved to from the current state
            self.__generate_safe_transitions__(state)
            #sort the child list in lexicographical order (in ascending order for numbers we use)
            self.nodes[state].child.sort()
            print("Child nodes of {}: {}".format(state,self.nodes[state].child))
            #if a child node of current state has not been visited or it is not in the queue already, add the child node to back of the queue
            print("Child nodes to be added to queue: ", end = "")
            for neighbour in self.nodes[state].child:
                if neighbour not in Queue.queue and neighbour not in self.visited: #there is no point adding a node to queue if it is already visited or already in the queue
                    Queue.add(neighbour)
                    #set the parent of neighbour as state to indicate that neighbour is added to queue as a child node of state
                    self.nodes[neighbour].set_parent(state)
                    print("'{}'".format(neighbour), end = " ")                    
            print("\nQueue: {}\n".format(Queue.queue))

# initialize the input variables for first question
cannibals = 5
missionaries = 5
boat_size = 3

print("State represantation used is a string consisting of number of cannibals on west, number of missonaries on west and boat pos(0 for west, 1 for east),respectively")

print("\n****Question 1****\n")
# create the search space for first question
first = Space(cannibals, missionaries, boat_size)
#solve the problem
first.solve()

# initialize the input variables for second question part a
cannibals = 6
missionaries = 6
boat_size = 4

print("\n****Second Question (2-a)****\n")
# create the search space for second question
second = Space(cannibals,missionaries,boat_size)
#solve the problem
second.solve()




