from config.dynamicSize import WR,FR,HR,fontToUse

from tkinter import *
from tkcalendar import DateEntry
from datetime import datetime

# Current date time in local system
print(datetime.now())
def navigationFrame(self,tab):

    def getDate():
        startDate = chooseStartDate.get_date()
        endDate = chooseEndDate.get_date()
        print(startDate,"to",endDate)

    def insertDate(e="" ,dateToInsert=""):
        if dateToInsert == "":
            today = datetime.date(datetime.now())
            print(today)
            chooseEndDate.set_date(today)
        else:
            dateToInsert = datetime.strptime(dateToInsert, '%y-%m-%d')
            chooseStartDate.set_date(dateToInsert)
    self.displayFrame = Frame(tab)
    self.displayFrame.pack(fill = 'both')

    descLabel = Label(self.displayFrame,text="Overview of Sales",font=(fontToUse,int(FR*20)))
    descLabel.pack()

    topFrame = Frame(self.displayFrame)
    topFrame.pack()
    
    fromLabel = Label(topFrame,text="From",font=(fontToUse,int(FR*10)))
    fromLabel.grid(row =  0 ,column= 0,padx=5)

    chooseStartDate = DateEntry(topFrame,width=12, background='darkblue',
                    foreground='hite', borderwidth=2, year=2021)
    chooseStartDate.grid(row = 0,column=1, padx = 5)
    day1Button = Button(topFrame,text="day1",command=lambda:insertDate("",day1Date))
    day1Button.grid(row=1,column=1)

    toLabel = Label(topFrame,text="To",font=(fontToUse,int(FR*10)))
    toLabel.grid(row = 0,column=3,padx=5)

    chooseEndDate = DateEntry(topFrame,width=12, background='darkblue',selectmode='day',
                    foreground='white', borderwidth=2, year=2021)
    chooseEndDate.grid(row = 0,column = 4,padx= 5)
    todayDateButton = Button(topFrame,text="today",command=insertDate)
    todayDateButton.grid(row=1,column=4)

    findButton = Button (topFrame,text = "Find",font = (fontToUse,int(FR*11)),command=getDate)
    findButton.grid(row = 0,column = 5,padx=5)
    

