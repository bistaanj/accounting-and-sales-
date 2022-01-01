from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from datetime import datetime
from config.dynamicSize import HR, WR, FR


def createNewRow(frame):
    frameBox = Frame(frame, bg = '#ffffff')
    frameBox.pack(pady = int(HR*10))
    uom_label = Label(
        frameBox, text=" UOM ", bg = "#ffffff", font = ('Comic Sans MS', int(FR*10)))
    uom_label.pack(side='left')
    uom_entry = Entry(frameBox, border=0,bg='#CED7D7',font = ('Comic Sans MS', int(FR*10)))
    uom_entry.pack(side='left')
    
    bue_label = Label(
        frameBox, text=" Base Unit Eqv. ", bg = "#ffffff", font = ('Comic Sans MS', int(FR*10)))
    bue_label.pack(side='left')
    bue_entry = Entry(frameBox, border=0,bg='#CED7D7',font = ('Comic Sans MS', int(FR*10)))
    bue_entry.pack(side='left')

    cpPerUnit_label = Label(
        frameBox, text=" CP per Unit ", bg = "#ffffff", font = ('Comic Sans MS', int(FR*10)))
    cpPerUnit_label.pack(side='left')
    cp_entry = Entry(frameBox, border=0,bg='#CED7D7',font = ('Comic Sans MS', int(FR*10)))
    cp_entry.pack(side='left')


    def deleteRow():
        pass 
    delete_btn = Button(frameBox, text = 'Delete', command=deleteRow)
    delete_btn.pack(side='left')

def countRows(InFrames,OutFrames):
    count = 0
    for x in InFrames.winfo_children():
        count+=1 
    if count<4:
        createNewRow(InFrames)
    else:
        messagebox.showerror('Invalid request', 'Limit exceeded')





    


