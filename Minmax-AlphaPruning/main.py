"""
The code that implements either minimax algorithm or alphabeta pruning algorithm 
upon the choice of user on a specific structure of search tree. The single stepping output 
is decided by the user, as well.
"""
import sys

class Node():
    """
    Class that represents a node in the search tree
    
    Attributes:
        node_id : The node name used for refferring to this node
        min_max : Node type (minimizer or maximizer)
        value : The integer value of the node either given as input or extracted by minimax and alphabeta algorithms
        move : Suggested move by minimax or alphabeta algorithms
        min : Minimum value that is updated during search if the node is a minimizer
        max : Maximum value that is updated during search if the node is a maximizer
        children : list of child nodes of current node
    """
    def __init__(self, node_id, min_max):
        self.node_id = node_id
        self.min_max = min_max
        self.value = 0
        self.move = None
        self.min = sys.maxsize #maximum integer value that the interpreter can have 
        self.max = -sys.maxsize #minimum integer value that the interpreter can have
        self.children = []
        
    def add_child(self,child):
        self.children.append(child)
    
    def set_value(self,value):
        self.value = value

    
class SearchTree():
    """
    The search tree for minimax and alphabeta algorithms. It has a specific type and has
    9 leaf nodes. The search tree is constructed by the given values of those leaf nodes.
    The tree structure and node names are available in single stepping output.
    
    Attributes:
        input_list : the list of values of leaf nodes in the order from A to I
        nodes : The dictionary that holds the nodes
        visited : The list to keep track of visited nodes during search
    """
    def __init__(self, input_list):
        self.input_list = input_list
        self.nodes = {}
        self.visited = []
        self.__create_nodes__()
        if single_stepping:
            print("\nSearch Tree is created\n")
            print("Search tree has the following format and node names\n")
            print("     " + str(0))
            print(" {}   {}   {}".format(1,2,3))
            print("ABC DEF GHI\n")
            
    def __create_nodes__(self):
        #create root node
        self.nodes[0] = Node(0, "max")
        #create intermediate minimizer nodes
        for i in range(1,4):
            self.nodes[i] = Node(i,"min")
            self.nodes[0].add_child(self.nodes[i])
        node_names = "ABCDEFGHI"
        k = 1
        #create the leaf nodes and set values of those leaf nodes
        for i in range(3):
            for j in range(3):
                self.nodes[node_names[3*i+j]] = Node(node_names[3*i+j],"max")
                self.nodes[k].add_child(self.nodes[node_names[3*i+j]])
                self.nodes[node_names[3*i+j]].set_value(self.input_list[3*i + j])
            k += 1        

    def minimax(self,node):
        """
        The function that implements minimax algorithm. It takes the root node as input
        and calls himself recursively until the leaf nodes are reached. Then it goes back
        to root node by deciding on the values of intermediate level(s). At the end, it 
        outputs the updated root node whose value and sugessted move is found
        
        Args:
            node (Node): Node object that the search is supposed to go from if not leaf node
        Returns:
            node (Node): Node object whose value and move are updated
        """
        #if the node is not a leaf node check its children to minimize or maximize
        if len(node.children) != 0:
            for child in node.children:    
                returned_node = self.minimax(child)
                score = returned_node.value
                move = returned_node.node_id
                
                if node.min_max == 'max':                    
                    #check if the child value is grater than current max
                    if score > node.max:
                        #if so, update max and move
                        node.max = score
                        node.move = move
                elif node.min_max == 'min':
                    #check if the child value is less than current min
                    if score < node.min:
                        #if so, update min and move
                        node.min = score
                        node.move = move
                        
                self.visited.append(child.node_id)
                if single_stepping:
                    print("Checked the child {} of node {}".format(child.node_id,node.node_id))
            #update the value of the node according to min or max value found among children
            if node.min_max == "max":
                node.value = node.max
            else:
                node.value = node.min
            if single_stepping:
                print("The value for node {} is {}\n".format(node.node_id,node.value))
            return node
        #if the node is a leaf node return the node which already has value
        else:
            return node

    def alphabeta(self,node, alpha, beta):
        """
        The function that implements alphabeta pruning algorithm. It takes the root node and alpha,
        beta values as inputand calls himself recursively until the leaf nodes are reached. 
        Then it goes backto root node by deciding on the values of intermediate level(s). It checks
        if the remaining children nodes can have an effect on the decison for the root node. If they
        can have no effect, it prunes them and doesn't visit them. At the end, it outputs the 
        updated root node whose value and sugessted move is found.
        
        Args:
            node (Node): Node object that the search is supposed to go from if not leaf node
        Returns:
            node (Node): Node object whose value and move are updated
        """
        #if the node is not a leaf node check its children to minimize or maximize
        if len(node.children) != 0:
            for child in node.children:  
                returned_node = self.alphabeta(child,alpha, beta)
                score = returned_node.value
                move = returned_node.node_id
                
                if node.min_max == 'max':
                    #check if the child value is grater than current max
                    if score > node.max:
                        #if so, update max and move
                        node.max = score
                        node.move = move
                        #update alpha value if node.max is grater than alpha
                        alpha = max(alpha,node.max)
                elif node.min_max == 'min':
                    #check if the child value is less than current min
                    if score < node.min:
                        #if so, update min and move
                        node.min = score
                        node.move = move
                        #update beta value if node.min is less than beta
                        beta = min(beta,node.min)
                self.visited.append(child.node_id)
                if single_stepping: 
                    print("Checked the child {} of node {}".format(child.node_id,node.node_id))
                #check if alpha greater than or equal to beta. If so, remaining children cannot change the decision for root node
                if alpha >= beta:
                    if single_stepping:
                        print("The remaining child nodes of node {} is not checked since {} >= {}".format(node.node_id,alpha,beta))
                    #since remaining children cannot change decision break the loop and prune those children nodes
                    break 
            #update the value of the node according to min or max value found among children        
            if node.min_max == "max":
                node.value = node.max
            else:
                node.value = node.min
            if single_stepping:
                print("The value for node {} is {}\n".format(node.node_id,node.value))
            return node
        #if the node is a leaf node return the node which already has value
        else:
            return node

    def solve(self, program):
        """
        The function that starts the algorithm and solves the problem. It prints the result to
        console (suggested move for MINIMAX, suggested move and pruned nodes for ALPHABETA).
        """
        if program == "MINIMAX":
            if single_stepping:
                print("Minimax algorithm is running\n")
            root = self.minimax(self.nodes[0])
        elif program == "ALPHABETA":
            if single_stepping:
                print("Alphabeta pruning algorithm is running\n")
            root = self.alphabeta(self.nodes[0], -sys.maxsize, sys.maxsize)
            print("Pruned nodes are", end = " ")
            for node in "ABCDEFGHI":
                if node not in self.visited:
                    print(node, end = " ")
            print()
        print("Move of the max player: " + "LMR"[root.move - 1])


global single_stepping
s_step = input("Do you want single stepping output? [y,n]: ")
if s_step == "y":
    single_stepping = True
else:
    single_stepping = False
        
program = input("Which program do you want? [MINIMAX, ALPHABETA]: ")

#solve the search trees given in hw assignment.(Given trees are already implemented in code)
if program == "MINIMAX":
    print('\n**********Search Tree 1**********\n')
    st1 = SearchTree([5,3,1,2,5,4,1,3,3])
    st1.solve(program)
    print("\n**********Search Tree 2**********\n")
elif program == "ALPHABETA":
    print("\n**********Search Tree 1**********\n")
    st1 = SearchTree([5,3,1,2,5,4,1,3,3])
    st1.solve(program)
    print("\n**********Search Tree 2**********\n")
    st2 = SearchTree([5,2,2,5,1,3,2,4,2])
    st2.solve(program)     
    print("\n**********Search Tree 3**********\n")
    st3 = SearchTree([1,3,4,1,4,1,3,5,3])
    st3.solve(program) 
    print("\n**********Search Tree4**********\n")

#take the input for user defined search tree and solve it  
inp = input("Enter 9 values seperated by space:\n")
input_list = list(map(int,inp.split(" "))) #convert the input to a list
st = SearchTree(input_list)
st.solve(program)