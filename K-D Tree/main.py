"""
The code that finds the nearest neighbour of an unknown point by querying a k-d tree. The k-d tree is
consturcted by the input values given in Winston p.404. The k-d procedure given in Winston p.408 is used
to query the tree and find the nearest neighbour. Single stepping is controlled via the single_stepping
variable.
"""
import statistics
import math
import sys

class node():
    """
    Class that represents a node to implement a tree
    
    Attributes:
        value: The threhold value that is calculated during the creation of tree
        axis: Represents the axis of comparison (1 for vertical, -1 for horizontal)
        data: The set of data points under this node
        parent: The parent node of the current node
        yes_child: The child node if the answer to comparison is yes
        no_child: The child node if the answer to comparison is no
    """
    def __init__(self,value,axis,data):
        self.value = value
        self.axis = axis
        self.data = data
        self.parent = None
        self.yes_child = None
        self.no_child = None
        
    def set_parent(self,parent):
        self.parent = parent
    def set_yes_child(self,child):
        self.yes_child = child
    def set_no_child(self,child):
        self.no_child = child
        
    def distance_to_boundary(self, unknown):
        """
        Function to calculate the minimum distance of unknown point to boundary point
        of the current region in the axis of comparison 
        
        Args:
            unknown (tuple): The unknown point with width and height given in a tuple
        Returns:
            min_dist (float): Min distance of unknown point to the points in the current set
                    in the axis of comparison
        """
        min_dist = sys.maxsize #maximum integer value that the interpreter can have 
        #check the axis of comparison for current desicion node
        if self.parent.axis == 1:
            #find the distance to boundary data point
            for el in self.data:
                if abs(el[2]-unknown[1]) < min_dist:
                    min_dist = abs(el[2]-unknown[1])
        elif self.parent.axis == -1:
            #find the distance to boundary data point
            for el in self.data:
                if abs(el[1]-unknown[0]) < min_dist:
                    min_dist = abs(el[1]-unknown[0])
        return min_dist
    
def calculate_median(data,axis):
    """
    Finds the median of data points in the desired axis and returns it
    
    Args:
        data (list): The set of points in the current region
        axis (int): The axis of comparison for current decision node
    Returns:
        median value of the heights or the widths according to the axis
    """
    if axis == 1:
        return statistics.median([point[2] for point in data]) 
    elif axis == -1:
        return statistics.median([point[1] for point in data])

def split_data(data,axis,median):
    """
    Splits the data 2 subsets by comparing to the median value and returns subsets
    
    Args:
        data (list): The set of points in the current region
        axis (int): The axis of comparison for current decision node
        median (float): median value in the axis of comparison
    Returns:
        subset1 (list): The list of points whose compared attribute is greater than median value
        subset2 (list): The list of points whose compared attribute is less than median value
    """
    if axis == 1:
        subset1 = [point for point in data if point[2] > median] 
        subset2 = [point for point in data if point[2] < median]
    elif axis == -1:    
        subset1 = [point for point in data if point[1] > median]
        subset2 = [point for point in data if point[1] < median]
    return subset1,subset2 

def hash_data(data):
    """
    Converts the list representation of data to string in order to have hashable reference to nodes
    """
    return str(data)

def build_tree(data,axis):
    """
    The procedure to build a decison tree for the given set of points and axis of comparison.
    The set of points are divided into two until there is only one elemet in the set. This
    function is used recursively to build the entire decision tree
    
    Args:
        data (list): The set of points in the current situation
        axis (int): The axis of comparison for current level
    """
    global nodes, single_stepping  
    if len(data) == 1:
        return None
    #find the median of points in the axis of comparison
    median = calculate_median(data,axis)
    #divide the current set into two subsets
    if single_stepping:
        print("\nAxis of comp: {}, Threshold: {}".format(axis,median))
    subset1, subset2 = split_data(data,axis,median)
    hashable_data = hash_data(data)
    #if the node has not been created previously (first call only)
    if hashable_data not in nodes.keys():
        nodes[hashable_data] = node(median,axis,data)
    
    #flip the axis of comparison
    axis *= -1   
    
    #get hashable versions of subsets to use as key reference
    hashable_s1 = hash_data(subset1)
    hashable_s2 = hash_data(subset2)
    
    #create the yes child which is the node that will be visited if the comparison is correct
    nodes[hashable_s1] = node(calculate_median(subset1,axis),axis,subset1)
    nodes[hashable_data].set_yes_child(nodes[hashable_s1])
    nodes[hashable_s1].set_parent(nodes[hashable_data])    
    
    #create the no child which is the node that will be visited if the comparison is wrong    
    nodes[hashable_s2] = node(calculate_median(subset2,axis),axis,subset2)
    nodes[hashable_data].set_no_child(nodes[hashable_s2])
    nodes[hashable_s2].set_parent(nodes[hashable_data])        

    #call same function recursively for subsets to move towards the leaf nodes 
    build_tree(subset1, axis)
    build_tree(subset2, axis)     


def kd_procedure(unknown,current_node,visited):
    """
    The procedure to query the decision tree and find the nearest neighbour to unknown point.
    The implementation of the pseudocode in Winston p.408. 
    
    Args:
        unknown (tuple): The unknown point with width and height given in a tuple
        current_node (node): The current node for which the comparison is being made
        visited (list): Set of nodes that has been visited by procedure
    Returns:
        likely (list): The set of likely points
        distance (float): Distance to the likely point
    """
    global single_stepping
    #if there is only one point under consideration, return likely set and distance
    if len(current_node.data) == 1:
        if single_stepping:
            print("Leaf node reached: {}".format(current_node.data[0]))
        return current_node.data[0], math.sqrt((current_node.data[0][1]-unknown[0])**2 + (current_node.data[0][2]-unknown[1])**2)
    
    #dive into decison tree by making comparisons until the leaf node is reached
    if current_node.axis == 1:
        #check if the statement for the current decison tree node is correct
        if unknown[1] > current_node.value:
            #go to yes child
            visited.append(current_node.yes_child)
            likely, distance = kd_procedure(unknown, current_node.yes_child,visited)
        else:
            #go to no child
            visited.append(current_node.no_child)
            likely, distance = kd_procedure(unknown, current_node.no_child,visited)   
    elif current_node.axis == -1:
        #check if the statement for the current decison tree node is correct
        if unknown[0] > current_node.value:
            #go to yes child
            visited.append(current_node.yes_child)
            likely,distance = kd_procedure(unknown, current_node.yes_child,visited)
        else:
            #go to no child
            visited.append(current_node.no_child)
            likely, distance = kd_procedure(unknown, current_node.no_child,visited)        
    
    #backtracing after leaf node is reached
    if current_node.no_child not in visited:
        #compare the current likely distance to boundary distance to other region
        if single_stepping:
            print("\nChecking distance <= boundary distance: {} <= {}".format(distance,current_node.no_child.distance_to_boundary(unknown)))
        if distance <= current_node.no_child.distance_to_boundary(unknown):
            return likely, distance
        else:
            #check the unlikely set using this procedure
            visited.append(current_node.no_child)
            unlikely, u_distance = kd_procedure(unknown, current_node.no_child,visited)
            #return the nearer of nearest neighbour in likely and unlikely set
            if u_distance < distance:
                return unlikely, u_distance
            else:
                return likely, distance
    else:
        #compare the current likely distance to boundary distance to other region
        if single_stepping:
            print("\nChecking distance <= boundary distance: {} <= {}".format(distance,current_node.yes_child.distance_to_boundary(unknown)))

        if distance <= current_node.yes_child.distance_to_boundary(unknown):
            return likely, distance
        else:
            #check the unlikely set using this procedure
            visited.append(current_node.yes_child)
            unlikely, u_distance = kd_procedure(unknown, current_node.yes_child,visited)   
            #return the nearer of nearest neighbour in likely and unlikely set
            if u_distance < distance:
                return unlikely, u_distance
            else:
                return likely, distance

single_stepping = True
nodes = {}
data = [("Red",1,2),("Violet",2,1),("Blue",4,2),("Green",6,1),("Orange",2,5),("Red",2,6),
        ("Yellow",5,6),("Purple",6,5)]

#build the k-d tree
if single_stepping:
    print("\n************Building k-d tree************\n")
    print("The representation of line drawings (1 for vertical axis, -1 for horizontal axis):")
build_tree(data,1)

#query 1
print("\n************Query 1************\n")
print("Unknown: (1,4)\n")
nearest_neighbour, dist = kd_procedure((1,4),nodes[str(data)],[nodes[str(data)]])
print("\nNearest neighbour is {} at {} with distance {}".format(nearest_neighbour[0],nearest_neighbour[1:],dist))

#query 2
print("\n************Query 2************\n")
print("Unknown: (1,1)\n")
nearest_neighbour, dist = kd_procedure((1,1),nodes[str(data)],[nodes[str(data)]])
print("\nNearest neighbour is {} at {} with distance {}".format(nearest_neighbour[0],nearest_neighbour[1:],dist))

#query 3
print("\n************Query 3************\n")
print("Unknown: (6,6)\n")
nearest_neighbour, dist = kd_procedure((6,6),nodes[str(data)],[nodes[str(data)]])
print("\nNearest neighbour is {} at {} with distance {}".format(nearest_neighbour[0],nearest_neighbour[1:],dist))

#query 4
print("\n************Query 4************\n")
print("Unknown: (6,1)\n")
nearest_neighbour, dist = kd_procedure((6,1),nodes[str(data)],[nodes[str(data)]])
print("\nNearest neighbour is {} at {} with distance {}".format(nearest_neighbour[0],nearest_neighbour[1:],dist))

#query 5
print("\n************Query 5************\n")
unknown = tuple(map(int,input("Enter width and hight seperated by space:\n").split()))
print("Unknown: {}\n".format(unknown))
nearest_neighbour, dist = kd_procedure(unknown,nodes[str(data)],[nodes[str(data)]])
print("\nNearest neighbour is {} at {} with distance {}".format(nearest_neighbour[0],nearest_neighbour[1:],dist))


