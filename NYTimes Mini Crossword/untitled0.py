"""
Several modules are merged so that it works in a single script. The explanation of used method
is given in the function explanations of puzzle object.
"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from googleapiclient.discovery import build
from datamuse import datamuse
import time
import itertools
from datetime import datetime
from tkinter import *

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
            
            temp =  word_domain("allintext:" + self.words[word_id].clue +' -crossword',self.words[word_id].length)
            temp2 = temp + word_domain(self.words[word_id].clue +' -crossword',self.words[word_id].length)
            domain = temp2 + data_muse(self.words[word_id].clue, self.words[word_id].length)
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
        
        max_satisfied = 0
        possible_words = words[:]
        for word in words:
            
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
                if num_of_satisfied >= max_satisfied:
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
        
    

def display_puzzle(cells, words, start_cells, single_stepping = False):
    def update_clock():
        global update
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        day.configure(text=now) 
        update = root.after(1000, update_clock)
    
    def on_closing():
        global update
        root.after_cancel(update)
        root.destroy()
    
    
    if single_stepping:
        print("Creating the gui window...")
    root = Tk()
    root.title('NYT Mini Puzzle')
    root.geometry('1175x500')


    left_window = Frame(root,width=330, height=330,borderwidth=50)
    left_window.grid(row = 0, column = 0)

    puzzle_grid = Label(left_window,text = "Official Solution",font =('Arial 12 bold'))
    puzzle_grid.grid(row = 0,column = 0,sticky=N)

    left_board = Canvas(left_window,width=301, height=301, borderwidth=0, highlightthickness=0)
    left_board.grid(row = 1,column = 0,sticky=N)#, fill="both", expand="true"
    
    clue_window = Frame(root)
    clue_window.grid(row = 0, column = 1)

    right_window = Frame(root,width=330, height=330,borderwidth=50)
    right_window.grid(row = 0, column = 2)    
    
    solvo_grid = Label(right_window,text = "AI Solution",font =('Arial 12 bold'))
    solvo_grid.grid(row = 0,column = 0,sticky=N)
    
    right_board = Canvas(right_window,width=301, height=301, borderwidth=0, highlightthickness=0)
    right_board.grid(row = 1,column = 0,sticky=N)#, fill="both", expand="true"    

    cellwidth = 60
    cellheight = 60
    if single_stepping:
        print("Displaying the puzzle grid with answers...")
    display_cells = {}
    labels = {}
    start_c = {}
    for i in range(25):
        row = i // 5
        column = i % 5
        x1 = column*cellwidth
        y1 = row * cellheight
        x2 = x1 + cellwidth
        y2 = y1 + cellheight
        if cells[i].correct_letter != None:
            display_cells[i] = left_board.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
            labels[i] = left_board.create_text((x1+30,y1+30), text=cells[i].correct_letter, font = "Arial 15")
            if i in start_cells.keys():
                start_c[i] = left_board.create_text((x1+5,y1+8), text= start_cells[i][0], font = "Arial 8")
        else:
            display_cells[i] = left_board.create_rectangle(x1,y1,x2,y2, fill="black", tags="rect")
    
    display_cells = {}
    s_labels = {}
    start_c = {}
    for i in range(25):
        row = i // 5
        column = i % 5
        x1 = column*cellwidth
        y1 = row * cellheight
        x2 = x1 + cellwidth
        y2 = y1 + cellheight
        if cells[i].correct_letter != None:
            display_cells[i] = right_board.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
            s_labels[i] = right_board.create_text((x1+30,y1+30), text=cells[i].letter, font = "Arial 15")
            if i in start_cells.keys():
                start_c[i] = right_board.create_text((x1+5,y1+8), text= start_cells[i][0], font = "Arial 8")
        else:
            display_cells[i] = right_board.create_rectangle(x1,y1,x2,y2, fill="black", tags="rect")
            s_labels[i] = right_board.create_text((x1+30,y1+30), text=cells[i].letter, font = "Arial 15")
    
    if single_stepping:
        print("Displaying clues...")
    accross_window = Frame(clue_window)
    accross_window.grid(row = 0, column = 0,sticky=W)
    
    across = Label(accross_window, text = "Across",font =('Arial 10 bold'))
    across.grid(row = 0,column = 0,sticky=W)
    
    down_window = Frame(clue_window)
    down_window.grid(row= 1, column= 0,sticky=W)
    
    down = Label(down_window, text = "Down",font =('Arial 10 bold'))
    down.grid(row = 0,column = 0,sticky=W)
    
    i, j = 1, 1
    for key in words.keys():
        if key[1] == "A":
            l1 = Label(accross_window, text = key[0] + " " + words[key].clue,wraplength = 400,justify=LEFT)
            l1.grid(row = i, column = 0,sticky=W)
            i += 1
        elif key[1] == "D":
            l1 = Label(down_window, text = key[0] + " " + words[key].clue,wraplength = 400,justify=LEFT)
            l1.grid(row = j, column = 0,sticky=W) 
            j += 1
    
    group_name = Label(left_window , text = "SOLVO")
    group_name.grid(row = 3,column = 0,sticky=NE)
    
    # datetime object containing current date and time
    now = datetime.now()
    day = Label(left_window , text = now.strftime("%d/%m/%Y %H:%M:%S"))
    day.grid(row = 2,column = 0,sticky=NE)
   
    if single_stepping:
        print("The gui window is ready and running...")
    
    update_clock()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def create_driver():
    if flag:
        print("\nInitializing the web driver...\n")
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    # driver.maximize_window()
    return driver


def get_to_the_page(driver):
    if flag:
        print('\nGoing to the "https://www.nytimes.com/crosswords/game/mini"...')
        driver.get("https://www.nytimes.com/crosswords/game/mini")
        ok = driver.find_element_by_css_selector('#root > div > div > div.app-mainContainer--3CJGG > div > main > div.layout > div > div.Veil-veil--3oKaF.Veil-stretch--1wgp0 > div.Veil-veilBody--2x-ZE.Veil-autocheckMessageBody--31wj3 > div > article > div.buttons-modalButtonContainer--35RTh > button')
        print('Arrived to the page trying to get ok button...')
        time.sleep(4)
        ok.click()
        print('Clicked to the ok button...')
    else:
        driver.get("https://www.nytimes.com/crosswords/game/mini")
        ok = driver.find_element_by_css_selector('#root > div > div > div.app-mainContainer--3CJGG > div > main > div.layout > div > div.Veil-veil--3oKaF.Veil-stretch--1wgp0 > div.Veil-veilBody--2x-ZE.Veil-autocheckMessageBody--31wj3 > div > article > div.buttons-modalButtonContainer--35RTh > button')
        time.sleep(3)
        ok.click()

def get_clues(driver):
    if flag:
        print("Downloading the clues...")
    clue_elements = driver.find_elements_by_class_name('Clue-text--3lZl7')
    across_clues = [element.text for element in clue_elements[:5]]
    down_clues = [element.text for element in clue_elements[5:]]
    if flag:
        print("Clues are downloaded...")
    return across_clues , down_clues

def reveal(driver):
    if flag:
        print("Revealing the answers before downloading puzzle grid...")
    reveal1 = driver.find_element_by_css_selector('#root > div > div > div.app-mainContainer--3CJGG > div > main > div.layout > div > div.Toolbar-wrapper--1S7nZ > ul > div.Toolbar-expandedMenu--2s4M4 > li:nth-child(2)')
    ac1 = ActionChains(driver)
    ac1.move_to_element(reveal1).move_by_offset(0, 0).click().perform()
    time.sleep(2)

    ac2 = ActionChains(driver)
    puzzle = driver.find_element_by_xpath( '//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a')
    ac2.move_to_element(puzzle).move_by_offset(0, 0).click().perform()
    time.sleep(2)

    ac3 = ActionChains(driver)
    reveal2 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/article/div[2]/button[2]/div/span')
    ac3.move_to_element(reveal2).move_by_offset(0, 0).click().perform()
    close_button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/span')
    close_button.click()

def get_answers(driver):
    if flag:
        print("Downloading the puzzle grid with answers...")
    cells = []

    for i in range(0,25):
        css_link = "".join(['#xwd-board > g:nth-child(5) > g:nth-child(', str(i + 1), ')'])
        if not driver.find_elements_by_css_selector(css_link):
            cells.append('')
        else:
            cells.append(driver.find_elements_by_css_selector(css_link)[0].text.split("\n"))

    cells_matrix = []
    for j in range(5):
        cells_matrix.append(cells[j*5:(j+1)*5])



    return cells_matrix



def conversion(cells_matrix,across,down):
    if flag:
        print("Converting the info to the form our system uses...")
    # Across Keys
    result = {}


    across_clues = {}
    across_values = {}
    across_keys = []

    for i in range(len(cells_matrix)):
        for j in range(len(cells_matrix[0])):
            if len(cells_matrix[i][j]) == 2:
                across_key_number = cells_matrix[i][j][0]
                across_index = 5*i + j
                across_key = across_key_number + 'A'
                across_keys.append(across_key)
                value = []
                value.append(across_index)
                answer = ''
                for k in range(j,5):
                    if len(cells_matrix[i][k]) == 2:
                        answer += cells_matrix[i][k][1]
                    elif len(cells_matrix[i][k]) == 1:
                        if cells_matrix[i][k][0] != '':
                            answer += cells_matrix[i][k][0]
                        else:
                            break
                value.append(answer)
                across_values[across_key] = value
                break


    across_keys.sort()
    for i in range(len(across_keys)):
        across_clues[across_keys[i]] = across[i]
    for i in range(len(across_values.keys())):
        x = across_values[across_keys[i]]
        x.append(across_clues[across_keys[i]])
        result[across_keys[i]] = x




    # Down Keys
    down_clues = {}
    down_values = {}
    down_keys = []

    for i in range(len(cells_matrix)):
        for j in range(len(cells_matrix[0])):
            if len(cells_matrix[j][i]) == 2:
                down_key_number = cells_matrix[j][i][0]
                down_index = 5*j + i
                down_key = down_key_number + 'D'
                down_keys.append(down_key)
                value = []
                value.append(down_index)
                answer = ''
                for k in range(j, 5):
                    if len(cells_matrix[k][i]) == 2:
                        answer += cells_matrix[k][i][1]
                    elif len(cells_matrix[k][i]) == 1:
                        if cells_matrix[k][i][0] != '':
                            answer += cells_matrix[k][i][0]
                        else:
                            break
                value.append(answer)
                down_values[down_key] = value
                break


    down_keys.sort()
    for i in range(len(down_keys)):
        down_clues[down_keys[i]] = down[i]
    for i in range(len(down_values.keys())):
        x = down_values[down_keys[i]]
        x.append(down_clues[down_keys[i]])
        result[down_keys[i]] = x
    return result

def download_puzzle(single_stepping = False):
    global flag
    flag = single_stepping
    driver = create_driver()
    get_to_the_page(driver)
    
    across, down = get_clues(driver)
    
    reveal(driver)
    
    cells_matrix = get_answers(driver)
    time.sleep(2)
    driver.close()
    result = conversion(cells_matrix,across,down)
    if flag:
        print("Input of the system is ready...")
    return result
            

#First
my_api_key3 =  "AIzaSyA8gwI2_EAyJPB_s5VjOov52DFxunQUHJI" #The API_KEY you acquired
my_cse_id3 =  "21714045fa03cc7bf" #The search-engine-ID you created


# #SECOND
my_api_key0 =  "AIzaSyAbNMviohZp1kO3dErSDTGJdujHpo_zkFU" #The API_KEY you acquired
my_cse_id0 =  "5c7c592812493a880" #The search-engine-ID you created

#third
my_api_key1 = "AIzaSyA8SvyXFLwXiA3Y3eesZTf9f24YYnjP1w0" #The API_KEY you acquired
my_cse_id1 = "b8e7e205f68568741" #The search-engine-ID you created

#fourth
my_api_key2 =  "AIzaSyBb_xxznvZZFzg4BiNkQ9vw3zKuP9L6baE" #The API_KEY you acquired
my_cse_id2 =  "52834ebca8cacf265" #The search-engine-ID you created

my_api_key = [my_api_key0,my_api_key1,my_api_key2,my_api_key3]
my_cse_id = [my_cse_id0,my_cse_id1,my_cse_id2,my_cse_id3]

api = datamuse.Datamuse()

def google_search(search_term, api_key, cse_id, i, **kwargs):
    try:
        service = build("customsearch", "v1", developerKey=api_key[i])
        res = service.cse().list(q=search_term, cx=cse_id[i], **kwargs).execute()
        if 'items' in res.keys():
            return res['items']
        else:
            return []
    except:
        i += 1
        print(i)
        if i <= 3:
            return google_search(search_term, api_key, cse_id, i)
        else:
            return []



def word_domain(clue, lenght):
    results = google_search(clue, my_api_key, my_cse_id, 0, num=10)

    res = []
    #for result in results:
        #print(result)

    for result in results:
        for word in result['snippet'].split():
            actual_word = ''
            for char in word:
                if char.isalpha():
                    actual_word += char
            if len(actual_word) == lenght:
                res.append(actual_word)
    #print(res)
    return res

def data_muse(clue,length):
    results = api.words(ml=clue)
    
    res = []
    for lst in results:
        word = lst['word']
        if len(word) == length:
            res.append(word)
    
    return res

               
single_stepping = True

#download puzzle info
puzzle_info = download_puzzle(single_stepping)

#construct puzzle object
puz = puzzle(puzzle_info,single_stepping)

#search clues via google api and datamuse api   
puz.search_clues()

#populate grid from domains
puz.solve()

#display the result
puz.create_display(single_stepping) 