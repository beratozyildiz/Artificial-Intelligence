# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 20:16:28 2020

@author: User
"""
from tkinter import *
from datetime import datetime


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




