import datetime
from tkinter import messagebox
from win32api import GetSystemMetrics, WinExec

def warnUser( text):
    messagebox.showinfo("Warning", text)

def getDateTime(self):
    nw = datetime.now(self)
    date = nw.strftime("%d/%m/%Y")
    time = nw.strftime("%H:%M")
    return (date,time)