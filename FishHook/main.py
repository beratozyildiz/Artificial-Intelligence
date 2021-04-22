"""
The code that implements fishhook algorithm to find the class precedence lists for a given
input tree. The input tree representation is assumed to be an edge list and the inputs
are created accordingly. The fishhook pairs found from the input edge list. Then, the class
precedence is found by applying fishhook algorithm. The output precedence list given in the console
contains classes from highest precedence to lowest.
"""

def extract_fishhook_pairs(tree,queue,fishhook):
    """
    The function that finds the fishhook pairs from a given tree with a root node 
    given in the queue. It goes up to Everything by recursion.
    
    Args:
        tree (list): Edge list of input tree
        queue (list): The queue that contains nodes that the algorithm should visit as a root 
                        (root node should be given in queue when calling from outside)
        fishhook (list): The list of fishhook pairs (empty when calling from outside)
    Returns:
        fishhook (list): The list of fishhook pairs 
    """
    #create list that will hold the nodes for which the 'vertical' pair is already created 
    nodes = []
    #take the first element in the queue as root node
    root = queue.pop(0)
    #if the algorithm reached everything class as root, return the fishhook pairs list
    if root == "Everything":
        return fishhook
    #iterate through the edge pairs in the edge list of input tree
    for pair in tree:
        #check if edge goes out from the current root node
        if pair[0] == root:
            #check if the first pair that goes up in tree is created 
            if pair[0] not in nodes:
                #create the fishhook pair that goes from root to upper level and add the root node to visited nodes
                nodes.append(pair[0])
                fishhook.append((pair[0],pair[1]))
                #add the child node to queue in order to visit on the next call
                if pair[1] not in queue:    
                    queue.append(pair[1])
                #hold the name of child node that will be the first element in the next pair creation
                temp = pair[1]
            else:
                #create the horizontal fishhook pair
                fishhook.append((temp, pair[1])) 
                #add the child node to queue in order to visit on the next call
                if pair[1] not in queue:    
                    queue.append(pair[1])
                #hold the name of child node that will be the first element in the next pair creation
                temp = pair[1]
    
    #return the same method with updated queue and fishhook list recursively
    return extract_fishhook_pairs(tree, queue,fishhook)
            

def break_tie(exposed,precedence,tree):
    """
    The function that sorts breaks a tie when there are more than 
    one exposed classes. It selects the class by checking if a class is a direct superclass of 
    the classes in the precedence list starting from the lowest precedence class.
    
    Args:
        exposed (list): list of exposed classes
        precedence (list): the precedence list so far
        tree (list): edge list representation of input tree
        
    Returns:
        node (string): the selected exposed class 
    """
    #reverse the precedence list to have the lowest precedence at the beginning
    reversed_list = precedence[::-1] 
    #check if the exposed class is a direct superclass of a class already in the precedence list (starting from lowest precedence)
    for el in reversed_list:
        for node in exposed:
            edge = [el,node]
            #if it is a direct superclass and not already in sorted exposed, than add it to sorted exposed list
            if edge in tree:
                return node

def find_precedence(tree,pairs):
    """
    The function that finds the precedence list given the tree and the fishhook pairs.
    
    Args:
        tree (list): Edge list of the input tree
        pairs (list): Fishhok pairs found previously for the specific root node
        
    Returns:
        precedence (list): The precedence list that contains class hierarchy from highest precedence to lowest.  
    """
    precedence = []
    #until all fishhook pairs are eliminated
    while len(pairs) != 0:
        first = []
        second = []
        exposed_list = []    
        #find exposed classes
        for pair in pairs:
            first.append(pair[0])
            second.append(pair[1])    
        for el in first:
            if el not in second and el not in exposed_list:
                exposed_list.append(el)
        if single_stepping: print("Exposed classes: ",exposed_list)
        
        #break tie if there are more than one exposed
        if len(exposed_list) > 1:
            exposed = break_tie(exposed_list,precedence,tree)
            if single_stepping: print("Selected class: ",exposed)
        else:
            exposed = exposed_list[0]
        
        #add the exposed class to precedence list
        precedence.append(exposed)
        temp_pairs = pairs[:]
        #eliminate pairs that contains this exposed class in the first element
        for pair in pairs: 
            # print("Initial pair: ", pair)
            if pair[0] == exposed:
                temp_pairs.remove(pair)
                if single_stepping:
                    print("removed pair: ",pair)
        if single_stepping:
            print()                    
        pairs = temp_pairs[:]
                    
    precedence.append("Everything")
    return precedence

def apply_fishhook(tree):
    """
    The function that applies fishhook algorithm to a tree by using other functions.
    It first finds the root nodes for which the class precedence list is to be found.
    Then, finds the class precedence list for all roots and prints them to console.
    
    Args:
        tree (list): The input tree represented as an edge list
    """
    roots = []
    first = []
    second = []
    #find the root nodes by checking first and second elements in the edge list
    for pair in tree:
        first.append(pair[0])
        second.append(pair[1]) 
    for el in first:
        if el not in second and el not in roots:
            roots.append(el)
    if single_stepping:
        print("Roots for this tree: ",roots)
    
    #apply fishhook algorithm for each root node in the tree
    for root in roots:
        pairs = []
        precedence = []
        #find fishhook pairs
        pairs = extract_fishhook_pairs(tree,[root],fishhook = [])
        if single_stepping:
            print("\n---------------\nFinding the precedence for: ",root,end = "\n\n")
            print("Fishhook pairs for {}:\n".format(root),pairs, end = "\n\n")
        #find and print the precdence list 
        precedence = find_precedence(tree, pairs)
        print("The precedence list for {}:\n".format(root),precedence,end ="\n\n")

#create input edge lists
tree_1 = [["ifstream","istream"],["istream","ios"],["fstream","iostream"],["iostream","istream"],
          ["iostream","ostream"],["ostream","ios"],["ofstream","ostream"],["ios","Everything"]]

tree_2 = [["Consultant Manager", "Consultant"],["Consultant Manager", "Manager"],["Consultant", "Temporary Employee"],
          ["Temporary Employee","Employee"],["Manager","Employee"],["Employee","Everything"],["Director","Manager"],
          ["Permanent Manager","Manager"],["Permanent Manager","Permanent Employee"],["Permanent Employee","Employee"]]

tree_3 = [["Crazy", "Professors"],["Crazy", "Hackers"], ["Professors","Eccentrics"],["Professors","Teachers"],
          ["Hackers","Eccentrics"],["Hackers","Programmers"],["Eccentrics", "Dwarfs"],["Teachers", "Dwarfs"],
          ["Programmers", "Dwarfs"],["Jacque","Weightlifters"],["Jacque","Shotputters"],["Jacque","Athletes"],
          ["Weightlifters","Athletes"],["Weightlifters","Endomorphs"],["Shotputters","Athletes"],
          ["Shotputters","Endomorphs"],["Athletes","Dwarfs"],["Endomorphs","Dwarfs"],["Dwarfs","Everything"]]  

single_stepping = True

#find class precedences by applying fishhook algorithm
print("\n****************Tree 1****************\n")
apply_fishhook(tree_1)
print("\n****************Tree 2****************\n")
apply_fishhook(tree_2)
print("\n****************Tree 3****************\n")
apply_fishhook(tree_3)

            