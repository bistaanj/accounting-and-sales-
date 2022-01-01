import pymongo
from datetime import datetime
from tkinter import messagebox
from win32api import GetSystemMetrics, WinExec
import win32api

def warnUser( text):
    messagebox.showinfo("Warning", text)

def getDateTime(self=""):
    nw = datetime.now()
    date = nw.strftime("%d/%m/%Y")
    time = nw.strftime("%H:%M")
    return (date,time)
    
def getUnitCostPrice(totalCostPRice,Quantity):
    return "{:.2f}".format(float(totalCostPRice) / int(Quantity))

def getConnect(database,collection):
    connection = pymongo.MongoClient('localhost',27017)
    # database = connection[self.activeDatabase]
    database = connection[database]
    # collection = database['inventory']
    collection = database[collection]
    # connection.close()
    return collection