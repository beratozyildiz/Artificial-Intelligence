import puzzle_updater
from solvo import word_domain


class Clue:
    def __init__(self, name, starting_cell, length, clue):
        self.name = name
        self.starting_cell = starting_cell
        self.length = length
        self.clue = clue
        self.occupied_cells = self.find_occupied_cells()
        self.domain = None

    def find_occupied_cells(self):
        if 'D' in self.name:
            occupied = [self.starting_cell]
            for i in range(1,self.length):
                o_cell = self.starting_cell + 5*i
                occupied.append(o_cell)
            return occupied
        if 'A' in self.name:
            occupied = [self.starting_cell]
            for i in range(1, self.length):
                o_cell = self.starting_cell + i
                occupied.append(o_cell)
            return occupied

puzzles = puzzle_updater.give_puzzles()
puzzle = puzzles['13/12/2020']
print(puzzle)


def initialize_clues():
    clues = []
    for i in puzzle.keys():
        x = Clue(i,puzzle[i][0],len(puzzle[i][1]),puzzle[i][2])
        x.domain = word_domain(x.clue +' -crossword',x.length)
        clues.append(x)
    return clues



clues = initialize_clues()
i = 0

for clue in clues:
    print(clue.domain)
    print()
    print('------')







