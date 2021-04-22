"""
The code that is used for random input state generation. The puzzles are generated with
10 random moves of the empty tile.
"""
import random
import numpy as np
goal_state = [[1,2,3,4],[2,3,4,5],[3,4,5,5],[4,5,5,0]]
arr = np.array(goal_state)

zero_pos = [3,3]
def possible_actions(zero_pos):
    """
    Finds and returns the possible actions for the current zero position
    
    Args:
        zero_pos (list): current position of zero  
    Returns:
        actions (list): list of possible actions
    """
    actions = ['u','d','l','r']
    if zero_pos[0] == 0:
        actions.remove('u')
    if zero_pos[1] == 0:
        actions.remove('l')
    if zero_pos[0] == 3:
        actions.remove('d')
    if zero_pos[1] == 3:
        actions.remove('r')
    return actions

def shuffle():
    """
    Shuffles the goal state by 10 random move and returns the resulting state
    
    Returns:
        state (array): the state reached after 10 random moves 
    """
    state = np.array([[1,2,3,4],[2,3,4,5],[3,4,5,5],[4,5,5,0]])
    zero_pos = [3,3]
    for i in range(10):
        pos_act = possible_actions(zero_pos)
        ind = random.randint(0, len(pos_act)-1)
        action = pos_act[ind]
        if action == 'u':
            state[zero_pos[0]][zero_pos[1]] ,state[zero_pos[0]-1][zero_pos[1]] = state[zero_pos[0]-1][zero_pos[1]],state[zero_pos[0]][zero_pos[1]] 
            zero_pos = [zero_pos[0]-1, zero_pos[1]]
        elif action == 'd':
            state[zero_pos[0]][zero_pos[1]] ,state[zero_pos[0]+1][zero_pos[1]] = state[zero_pos[0]+1][zero_pos[1]],state[zero_pos[0]][zero_pos[1]]
            zero_pos = [zero_pos[0]+1, zero_pos[1]]
        elif action == 'l':
            state[zero_pos[0]][zero_pos[1]] ,state[zero_pos[0]][zero_pos[1]-1] = state[zero_pos[0]][zero_pos[1]-1],state[zero_pos[0]][zero_pos[1]]
            zero_pos = [zero_pos[0], zero_pos[1]-1]
        else:
            state[zero_pos[0]][zero_pos[1]] ,state[zero_pos[0]][zero_pos[1]+1] = state[zero_pos[0]][zero_pos[1]+1],state[zero_pos[0]][zero_pos[1]]
            zero_pos = [zero_pos[0], zero_pos[1]+1]
    return state
        # print(state)
def generate_states():
    """
    Generates and returns 12 distinct states that is found by 10 random move of empty tile
    
    Returns:
        inputs (list): the list of 12 input states
    """
    goal_state = np.array([[1,2,3,4],[2,3,4,5],[3,4,5,5],[4,5,5,0]])
    states = [goal_state]
    while len(states) < 13:
        candidate = shuffle()
        different = True
        for state in states:
            if np.sum(candidate == state) == 16:
                different = False
                break
        if different:
            states.append(candidate)
    states.remove(goal_state)
    inputs = []
    for state in states:
        inputs.append(np.ndarray.tolist(state))
    return inputs


            
            
            
            
            
            