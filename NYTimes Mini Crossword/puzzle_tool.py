# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 18:09:59 2020

@author: User
"""
from gui_tool import *
from solvo import *
import itertools
from clue_filter import pop_backslash

class constraint():
    def __init__(self,matching_letters,words):
        self.matching_letters = matching_letters
        self.__generate_constraint__(words)
        
    def __generate_constraint__(self,words):
        self.word1 = self.matching_letters[0][0]
        self.word1_ind = self.matching_letters[0][1]
        self.word2 = self.matching_letters[1][0]
        self.word2_ind = self.matching_letters[1][1]
        
    def check_constraint(self,possible_word1,possible_word2):
        return possible_word1[self.word1_ind] == possible_word2[self.word2_ind]


class cell():
    def __init__(self, cell_id, correct_letter = None, letter = None):
        self.cell_id = cell_id
        self.correct_letter = correct_letter
        self.letter = letter
        self.words = []
        # converter = {0 : (0,0), 1: (0,1), 2: (0,2)}
    def set_correct_letter(self,letter,word_id,index):
        self.correct_letter = letter
        self.words.append((word_id,index))
    def assign_letter(self, letter):
        self.letter = letter


class word():
    def __init__(self, word_id, length, start_cell, clue, correct_word = "", word = ""):
        self.word_id = word_id
        self.length = length
        self.start_cell = start_cell
        self.direction = word_id[1]
        self.clue = clue
        self.correct_word = correct_word
        self.word = word
        self.letter_ids = []
        self.find_cells()
        self.domain = []
        self.constraints = []
        self.see = False
        self.wth = False
        self.__is_connected__()
    def set_correct_word(self,word):
        if len(word) == self.length:
            self.correct_word = word
            self.set_correct_cells()
      
    def assign_word(self, word,cells):
        if len(word) == self.length:
            self.word = word
            self.set_cells(cells)
        
    def find_cells(self):
        for i in range(len(self.correct_word)):
            if self.direction == "A":
                self.letter_ids.append(self.start_cell + i)
            elif self.direction == "D":
                self.letter_ids.append(self.start_cell + 5*i)

    def set_cells(self,cells):
        for i in range(len(self.word)):
            cells[self.letter_ids[i]].assign_letter(self.word[i])
    
    def set_correct_cells(self,cells):
        for i in range(len(self.correct_word)):
            cells[self.letter_ids[i]].set_correct_letter(self.correct_word[i],self.word_id,i)
            # cells[self.letter_ids[i]].set_word(self.)
            
    def assign_word_domain(self,domain):
        print("\nDomain for {}: {}".format(self.word_id,domain))
        self.domain = domain
    
    def add_constraint(self,const):
        self.constraints.append(const)
    
    def __is_connected__(self):
        if "See" in self.clue:
            if "-down" in self. clue or "-across" in self.clue:
                self.see = True
        if "With" in self.clue:
            if "-down" in self. clue or "-across" in self.clue:
                self.wth = True
class puzzle():
    def __init__(self, puzzle_info, single_stepping = False ):
        if single_stepping:
            print("Constructing the puzzle object...")
        self.puzzle_info = puzzle_info
        self.cells = {}
        self.words = {}
        self.across = {}
        self.down = {}
        self.start_cells = {}
        self.__construct_cells__()
        self.__construct_words__()
        self.generate_constraints()
        self.seperate_by_direction()
        if single_stepping:
            print("Puzzle object is ready...")
        # print(self.cells[11].words)
        
    def __construct_cells__(self):
        for i in range(25):
            self.cells[i] = cell(i)
        
    def __construct_words__(self):
        for word_id in self.puzzle_info:
            correct_answer = self.puzzle_info[word_id][1]
            length = len(correct_answer)
            start_cell = self.puzzle_info[word_id][0]
            self.start_cells[start_cell] = word_id
            clue = self.puzzle_info[word_id][2]
            self.words[word_id] = word(word_id, length,start_cell, clue, correct_answer)        
            self.words[word_id].set_correct_cells(self.cells)
            # {"1D" : [start_cell, correct_answer, clue],"1A": }
    
        
    def create_display(self, single_stepping):
        display_puzzle(self.cells,self.words, self.start_cells,single_stepping)
        
    def generate_constraints(self):
        for cell in self.cells.keys():
            overlap = self.cells[cell].words
            if len(overlap) != 0:
                const = constraint(overlap,self.words)
                for el in overlap:
                    self.words[el[0]].add_constraint(const)
    def seperate_by_direction(self):
        for word_id in self.words.keys():
            if word_id[1] == "A":
                self.across[word_id] = self.words[word_id]
            elif word_id[1] == "D":
                self.down[word_id] = self.words[word_id]
             
  
    def search_clues(self):
        """
        Funciton that searches the clues via Google api and datamuse api. It sets the domain
        of relevant word_id to the search results
        """
        print("\n************Searching Clues************\n")
        for word_id in self.words.keys():
            if not self.words[word_id].see and not self.words[word_id].wth:
                clue = pop_backslash(self.words[word_id].clue)
                temp =  word_domain("allintext:" + clue +' -crossword',self.words[word_id].length)
                temp2 = temp + word_domain(clue +' -crossword',self.words[word_id].length)
                domain = temp2 + data_muse(clue, self.words[word_id].length)
                unique_list = []
                for x in domain: 
                    y = x.upper()
                    # check if exists in unique_list or not 
                    if y not in unique_list: 
                        unique_list.append(y) 
            
                self.words[word_id].assign_word_domain(unique_list)
        print("\nSearch is done...")
    def get_length(self,word_id):
        # print("{}: {}".format(word_id,len(self.words[word_id].constraints)))
        return self.words[word_id].length
    
    def satisfied_constraints(self,word_id, possible_word):
        """
        Fuction that finds the words that satisfy the letters of possible_word which is a
        possible answer for word_id ('1A' for 1-across,'2D' for 2-down etc.) It returns a dictionary
        whose key is the word_id2 which crosses one of the letters of input word_id, and whose value
        is a list of words (from the word_id2) that satisfy that letter for possible_word.
        
        Args:
            word_id (string): ('1A' for 1-across,'2D' for 2-down etc.)
            possible_word (string): a word from the domain of 
        Returns:
            results (dict): dictionary that holds crossed word ids and possible words for that crossed word ids.
        """
        constraints = self.words[word_id].constraints
        results = {}
        # print("word_id: {}, possible_word: {}, visited: {}, num_of_satisfied: {}".format(word_id, possible_word, visited, num_of_satisfied))  
        for constraint in constraints:
            possibilities = []
            if word_id == constraint.word1:
                for possible_word2 in self.words[constraint.word2].domain:
                    check = constraint.check_constraint(possible_word,possible_word2)
                    if check:
                        possibilities.append(possible_word2)
                if len(possibilities) != 0:
                    results[constraint.word2] = possibilities
            elif word_id == constraint.word2:
                for possible_word2 in self.words[constraint.word1].domain:
                    check = constraint.check_constraint(possible_word2,possible_word)
                    if check:
                        possibilities.append(possible_word2)
                if len(possibilities) != 0:
                    results[constraint.word1] = possibilities
        return results
    
    def get_max_score(self,word_id, assigned_words):
        """
        A fuction that finds words that fit the current grid situation as much as possible
        It inputs a word_id and assigned_words that are assigned so that the constraints of 
        word_id possible word is satisfied. For instance for one across word, a possible word is 
        picked before this function and down words are assigned according to that across word.
        This function finds words that satisfy maximum constraints for other across words and
        returns the new found words with their number of satisfied constraints
        
        Args:
            word_id (string): ('1A' for 1-across,'2D' for 2-down etc.)
            assigned_words (dict): assigned words that represents current grid situation
        
        Returns:
            new_assigned_words (dict): words that fits the current grid best
            total_score (int): score that shows the number of satisfiable constraints for current grid
        """
        def find_max(possible_word_dict,word_id2):
            max_score = 0
            new_word_to_assign = '*' * self.words[word_id2].length
            for possible_word in possible_word_dict.keys():
                score = 0
                for element in assigned_words.keys():
                    if element != word_id2:
                        if element in self.satisfiers[word_id2][possible_word].keys():
                            if assigned_words[element] in self.satisfiers[word_id2][possible_word][element]:
                                score += 1
                if score >= max_score:
                    max_score = score
                    new_word_to_assign = possible_word
            return (new_word_to_assign, max_score), max_score
        if word_id[1] == 'A':
            words = self.across
        elif word_id[1] == 'D':
            words = self.down
        total_score = 0
        new_assigned_words = {}
        for word_id2 in words.keys():
            if word_id2 != word_id:
                max_w, max_s = find_max(self.satisfiers[word_id2],word_id2)
                total_score += max_s
                new_assigned_words[word_id2] = max_w
        return new_assigned_words, total_score
    
    def evaluate_score(self,word_id):
        """
        Function that finds the best satisfiers other than given word_id in the direction
        of word_id. It searches all possible words of word_id and it fills the other direction words
        that satisfy the constraints for particular possible word and then finds other non-assigned words
        that maximize satisfied constraints. And we obtain a confidence value for those previously non-assigned
        words
        
        Args:
            word_id (string): ('1A' for 1-across,'2D' for 2-down etc.)
            
        Returns:
            assigned_to_return (dict): Previously non-assigned words with their confidence value
            total_best (int): Total score of those newly assigned words
        """
        total_best = 0
        assigned_to_return = {}
        for possible_word in self.satisfiers[word_id].keys():
            words_to_iterate = []
            iterated_word_ids = []
            # print()
            for connected_word_id in self.satisfiers[word_id][possible_word].keys():
                words_to_iterate.append(self.satisfiers[word_id][possible_word][connected_word_id])
                # print("word_id: {}, possible_word: {}, connected_id: {}, words: {}".format(word_id,possible_word, connected_word_id,self.satisfiers[word_id][possible_word][connected_word_id]))
                iterated_word_ids.append(connected_word_id)
            
            # print(possible_word)
            # print("\nPossible word:",possible_word)
            for comb in itertools.product(*words_to_iterate):
                assigned_words = {}
                assigned_words[word_id] = possible_word
                for i in range(len(iterated_word_ids)):
                    assigned_words[iterated_word_ids[i]] = comb[i]
                # print("word_id: {} comb: {}".format(word_id,comb))
                # print("\nword_id: {}, assigned words: {}".format(word_id,assigned_words))
                new_assigned, current_max = self.get_max_score(word_id,assigned_words)
                # print("new_assigned: {}, current_max: {}".format(new_assigned, current_max))
                if current_max > total_best:
                    total_best = current_max
                    assigned_to_return = {}
                    assigned_to_return = new_assigned
        return assigned_to_return, total_best
            
            
    def check_grid(self,word_id, words, high_conf):
        """
        Function that checks the grid during the population of grid and allows
        words that fit the current grid and words that have hihgest confidence value
        if boolean high_conf is True.
        
        Args:
            word_id (string): ('1A' for 1-across,'2D' for 2-down etc.)
            words (list): list of words that have the same confidence value for word_id (max for that word_id)
            high_conf (boolean): flag that indicates if the given set of words are the highest confidence among all word_ids
        
        Returns:
            False if words violate current grid, True if there is no violation
            None if there is no satisfied confidence either or it's not highest confidence, word that fits otherwise            
        """
        assign = None
        max_satisfied = 0
        possible_words = words[:]
        for word in words:
            if high_conf:
                assign = word  
            num_of_satisfied = 0
            constraints = self.words[word_id].constraints
            for constraint in constraints:
                if word_id == constraint.word1:
                    if len(self.words[constraint.word2].word) != 0:
                        flag = constraint.check_constraint(word,self.words[constraint.word2].word)
                        if not flag:
                            possible_words.remove(word)
                            break
                        num_of_satisfied += 1
                elif word_id == constraint.word2:
                    if len(self.words[constraint.word1].word) != 0:
                        flag = constraint.check_constraint(self.words[constraint.word1].word,word)
                        if not flag:
                            possible_words.remove(word)
                            break
                        num_of_satisfied += 1
            if word in possible_words:
                if num_of_satisfied > max_satisfied:
                    assign = word
                    max_satisfied = num_of_satisfied
       
        if len(possible_words) == 0:
            return False, None
        elif max_satisfied > 0 or high_conf:                
            return True, assign
        else:
            return True, None
                        
                
    
    def solve(self):
        """
        Function that performs the solution by using other functions and filss the grid accordingly
        """
        words = list(self.words.keys())
        words.sort(key= self.get_length,reverse = True)
        self.satisfiers = {}
        print("\nTrying to populate the grid...")
        for word_id in words:
            self.satisfiers[word_id] = {}
            for possible_word in self.words[word_id].domain:
                result = self.satisfied_constraints(word_id,possible_word)
                self.satisfiers[word_id][possible_word] = result
                # print("\nword_id: {}, possible_word: {}, result: {}".format(word_id,possible_word, result))
                
        final_answers = {}
        highest_conf = 0
        for word_id in words:
            found_words,score = self.evaluate_score(word_id)
            # print("\nword_id: {}, found: {}, score: {}".format(word_id,found_words,score))
            for el in found_words.keys():
                if el in final_answers.keys():
                    if found_words[el][1] > final_answers[el][0]:
                        final_answers[el] = [found_words[el][1],found_words[el][0]]
                    elif found_words[el][1] == final_answers[el][0] and found_words[el][0] not in final_answers[el]:
                        final_answers[el].append(found_words[el][0])
                else:
                    final_answers[el] = [found_words[el][1],found_words[el][0]]
                if final_answers[el][0] > highest_conf:
                    highest_conf = final_answers[el][0] 
        print()
        print(final_answers)        
        
        #sort the elements of dictionary so that highest confidence comes first in for loop
        final_answers = {k: v for k, v in sorted(final_answers.items(), key=lambda item: item[1][0],reverse=True)}
        secondary = dict(final_answers)
        #first run that we restrict the confidence to be minimum 50%
        for key in final_answers.keys():
            if final_answers[key][0] >= self.words[key].length/2:
                high_conf = final_answers[key][0] == highest_conf
                check, word = self.check_grid(key,final_answers[key][1:],high_conf)
                if check:
                    if word != None:
                        self.words[key].assign_word(word,self.cells)
                        print("Assigned word for {}: {}".format(key,word))
                        secondary.pop(key)
        
        #secondary run that any confidence value can be assigned 
        for key in secondary.keys():
            if secondary[key][0] > 0:
                check, word = self.check_grid(key,secondary[key][1:],False)
                if check:
                    if word != None:
                        self.words[key].assign_word(word,self.cells)
                        print("Assigned word for {}: {}".format(key,word))
        
        
        

               
            
               
               
               
               
