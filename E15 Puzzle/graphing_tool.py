"""
The code that is used for graphing the steps of 2 solutions. It uses the pygame library to
visualize the puzzles. It requires a screen resolution of at least 1475x768 to fit in the screen.
"""

import sys
import pygame  # We used pygame library to visualize the puzzle
from pygame.locals import *
import threading
import time

pygame.init()
SCREEN = (1475, 768) # The screen pixels are selected specifically for laptop resolutions
WINDOW = pygame.display.set_mode(SCREEN) # It displays a window with selected resolution
FONT = pygame.font.SysFont("Helvetica", 24) # Font and fontsize decleration
ARROW = pygame.font.SysFont("Helvetica", 48) # Font and fontsize decleration
ARROWFONT = ARROW.render(">", 1, (255, 255, 255), (0, 0, 0)) # It prepares the symbol of ">" to display
SOL1 = FONT.render("SOLUTION FOR S1", 1, (255, 255, 255), (0, 0, 0)) # It prepares the symbol of "SOLUTION FOR S1" to display
SOL2 = FONT.render("SOLUTION FOR S2", 1, (255, 255, 255), (0, 0, 0)) # It prepares the symbol of "SOLUTION FOR S1" to display
pygame.display.set_caption('E15 PUZZLE') # Screen caption name
def createBoard(numberArray, bigX, bigY, x, y, index=0): # It creates a puzzle board according to given parameters
    pygame.draw.rect(WINDOW, (255, 255, 255), Rect((bigX, bigY), (145, 145)), 1) # It creates outer shell for puzzle
    basex = x # It initializes new int to return first x value at the end of every "for" loop
    for i in range(4):
        for l in range(4):
            if numberArray[index] != 0:
                pygame.draw.rect(WINDOW, (255, 255, 255), Rect((x, y), (30, 30)), 0) #If number is not 0 then draws a tile for puzzle
                WINDOW.blit(FONT.render(str(numberArray[index]), 1, (0, 0, 0), (255, 255, 255)), (x + 7, y)) # It puts the number inside of the tile
            index += 1 # It increases the index of array
            x += 35 # For x axis it pushes 35 pixel for new tile
        x = basex # It Returns the first location of the tile
        y += 35 # For y axis it pushes 35 pixel for new tile


def createArrow(direction, x, y): # It creates string representation of the tile movement result
    WINDOW.blit(FONT.render(direction, 1, (255, 255, 255), (0, 0, 0)), (x, y)) # It creates a string for the screen for which tile moved
    WINDOW.blit(ARROWFONT, (x + 7, y + 30)) # it creates ">" symbol for representation

def createSolutionText(): # It creates the headers for every solution
    WINDOW.blit(SOL1, (550, 5)) # It shows the "SOLUTION FOR S1" header for the first solution
    WINDOW.blit(SOL2, (550, 380)) # It shows the "SOLUTION FOR S2" header for the second solution


def draw_graph(solutions,moves ):
    while True: # It keeps the screen open during the operations
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit # It exits when user click the "X" button at top
            createSolutionText() # It envokes the specified function
            a = 40 # First Location of the axis
            d = 40 # First Location of the axis
            b = 45 # First Location of the axis
            c = 45 # First Location of the axis
            
            ab_inc = [0,250,500,750,1000,1250] # Integer values for pushing the axis to create specified puzzles
            for sol in solutions:
                for i in range(len(sol)):
                    if i < 5:
                        createBoard(sol[i], a+ab_inc[i], d, b+ ab_inc[i], c) # It envokes the specified function
                    elif i < 11:
                        createBoard(sol[i], a+ab_inc[i-5], d + 180, b+ ab_inc[i-5], c +180) # It envokes the specified function
                d = d + 380
                c = c + 380
                
            x = [200,450,700,950,1200]  # Integer values for pushing the axis to create specified arrows
            y = 70
            for move in moves:
                for i in range(len(move)):
                    if i < 5:
                        createArrow(move[i], x[i], y) # It envokes the specified function
                    elif i < 10:
                        createArrow(move[i], x[i-5], y+180) # It envokes the specified function
                y = 470
        pygame.display.update()

class new_thread(threading.Thread):
   def __init__(self, threadID, name, solutions_to_graph, moves_to_graph):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.solutions_to_graph = solutions_to_graph
      self.moves_to_graph = moves_to_graph

   def run(self):
       demonstrate(self.solutions_to_graph,self.moves_to_graph)

def demonstrate(solutions_to_graph, moves_to_graph):
    time.sleep(0.3)
    draw_graph(solutions_to_graph, moves_to_graph)