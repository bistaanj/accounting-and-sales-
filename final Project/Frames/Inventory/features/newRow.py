from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from datetime import datetime
from config.dynamicSize import HR, WR, FR


def createNewRow(self,frame):
    frameBox = Frame(frame, bg = '#ffffff')
    frameBox.grid(pady = int(HR*10))
    uom_label = Label(
        frameBox, text=" UOM ", bg = "#ffffff", font = ('Comic Sans MS', int(FR*10)))
    uom_label.grid(row = self.rownum,column = 0)
    uom_entry = Entry(frameBox, border=0,bg='#CED7D7',font = ('Comic Sans MS', int(FR*10)))
    uom_entry.grid(row = self.rownum,column = 1)
    
    bue_label = Label(
        frameBox, text=" Base Unit Eqv. ", bg = "#ffffff", font = ('Comic Sans MS', int(FR*10)))
    bue_label.grid(row = self.rownum,column = 2)
    bue_entry = Entry(frameBox, border=0,bg='#CED7D7',font = ('Comic Sans MS', int(FR*10)))
    bue_entry.grid(row = self.rownum,column = 3)

    cpPerUnit_label = Label(
        frameBox, text=" CP per Unit ", bg = "#ffffff", font = ('Comic Sans MS', int(FR*10)))
    cpPerUnit_label.grid(row = self.rownum,column = 4)
    cp_entry = Entry(frameBox, border=0,bg='#CED7D7',font = ('Comic Sans MS', int(FR*10)))
    cp_entry.grid(row = self.rownum,column = 5)

    def deleteRow():
        self.rownum-=1
        rownum = delete_btn.grid_info()['row']
        widget = frame.grid_slaves(row=rownum)
        for x in widget:
            x.destroy()
    delete_btn = Button(frameBox, text = 'Delete', command=deleteRow)
    delete_btn.grid(row = self.rownum,column = 6)
    self.rownum +=1

def countRows(self,InFrames,OutFrames):
    count = 0
    for x in InFrames.winfo_children():
        count+=1 
    if count<4:
        createNewRow(self,InFrames)
    else:
        messagebox.showerror('Invalid request', 'Limit exceeded')





    


