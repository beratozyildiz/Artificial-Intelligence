# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 21:27:01 2020

@author: User
"""
from utilities import *
import pickle


result = download_puzzle(True)

# print(result) 

a_file = open("puzzles.pkl", "rb")
output = pickle.load(a_file)
# print(output)
output["20/12/2020"] = result
a_file.close()

a_file = open("puzzles.pkl", "wb")
pickle.dump(output, a_file)
a_file.close()

a_file = open("puzzles.pkl", "rb")
output = pickle.load(a_file)
print(output)
a_file.close()
print()
print(len(output.keys()))
print(list(output.keys()))
def give_puzzles():
    a_file = open("puzzles.pkl", "rb")
    output = pickle.load(a_file)
    a_file.close()
    return output