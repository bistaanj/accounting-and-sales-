from tkinter import ttk
from bson.objectid import ObjectId
from config.dynamicSize import WR,FR,HR,fontToUse,day1Date
from Frames.supportingFunctions import warnUser
from Frames.getConnect import getConnect
from tkinter import *
from tkcalendar import DateEntry
from datetime import datetime

# Current date time in local system
def navigationFrame(self,tab):
    def insertDate(e="" ,dateToInsert=""):
        if dateToInsert == "":
            today = datetime.date(datetime.now())
            chooseEndDate.set_date(today)
        else:
            dateToInsert = (dateToInsert, '%y-%m-%d')
            chooseStartDate.set_date(dateToInsert)
    
    def insertInTable(listForTable):
        count = 0
        for rows in viewTree.get_children():
            viewTree.delete(rows)

        for values in listForTable:
            viewTree.insert(parent='', index=END,
                        text=(count+1),
                        values=(
                    values["Product Name"],
                    values['Cost Price'],
                    values['Current Stock'],
                    values['Stock'],
                    values['Sold'],
                    values['Stock Value']
                    ))
            count+=1

    def getDateAndShowToTable():
        descriptionLabel.config(text="The stock of products in your shop from  " + chooseStartDate.get() + "  to  " + chooseEndDate.get() +"  is:")
        startDate = chooseStartDate.get_date()
        endDate = chooseEndDate.get_date()
        if endDate > datetime.date(datetime.now()) :
            warnUser("invalid Date Provided")
        else:
            collection1 = getConnect('saiRecords',"restock")
            collection2 = getConnect('saiRecords',"inventory")
            result = collection1.find()
            listForTable = []
            for i in result:
                rawData = {}
                stock = 0
                TS = 0    #total stock
                for key in list(i):
                    if key != "_id":
                        TS+=int(i[key]["Quantity"])
                        d = datetime.date(datetime.strptime(key[0:8],'%d%m%Y'))
                        if(d <= endDate and d >= startDate):
                            iid = i[key]["Product"]
                            stock+=int(i[key]["Quantity"])
                            product = collection2.find_one({"_id":ObjectId(iid)})
                            rawData["_id"] = product["_id"]
                            rawData["Product Name"] = product["Product Name"]
                            rawData["Current Stock"] = product["Quantity"]
                            rawData["Cost Price"]  = product["Cost Price"]
                            rawData["Sold"] = product["Sold"]
                if rawData:
                    rawData["Stock"] = stock
                    rawData["Stock Value"] = int(stock) * float(rawData['Cost Price'])
                    listForTable.append(rawData)
            insertInTable(listForTable)        

    self.displayFrame = Frame(tab)
    self.displayFrame.pack(fill = 'both')

    descLabel = Label(self.displayFrame,text="Overview of Stocks",font=(fontToUse,int(FR*20)))
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

    findButton = Button (topFrame,text = "Find",font = (fontToUse,int(FR*11)),command=getDateAndShowToTable)
    findButton.grid(row = 0,column = 5,padx=5)
    
    # GuI for overView Table 

    # detailsFrame = Frame(self.displayFrame)
    # detailsFrame.pack()

    descriptionLabel = Label(topFrame,text="The stock of products in your shop from  " + chooseStartDate.get() + "  to  " + chooseEndDate.get() +"  is:",font= (fontToUse,int(FR*15)))
    descriptionLabel.grid(columnspan=10,pady=12)


    tableFrame = Frame(self.displayFrame)
    tableFrame.pack()

    viewTree = ttk.Treeview(tableFrame, height = int(HR*10), style="mystyle.Treeview")
    #Define Columns
    viewTree['columns']= ('Product Name','Cost Price','Current Stock', 'Stock','Stock Value')
    viewTree.column('#0', width = int(WR*50), minwidth = int(WR*40), anchor = CENTER)
    viewTree.column('Product Name', width = int(WR*250),minwidth= int(WR*200), anchor = 'w')
    viewTree.column('Cost Price', width = int(WR*130),minwidth = int(WR*100), anchor=CENTER)
    viewTree.column('Current Stock', width = int(WR*130),minwidth = int(WR*120), anchor = CENTER)
    viewTree.column('Stock', width = int(WR*80),minwidth=int(WR*60), anchor = CENTER)
    # viewTree.column('Sold', width = int(WR*80),minwidth=int(WR*60), anchor=CENTER)
    viewTree.column('Stock Value', width = int(WR*200),minwidth=int(WR*180), anchor=CENTER)

    #Create Headings
    viewTree.heading('#0',text='S.N', anchor = CENTER)
    viewTree.heading('Product Name', text='Product Name',anchor = CENTER)
    viewTree.heading('Cost Price', text='Cost Price', anchor=CENTER)
    viewTree.heading('Current Stock', text='Current Stock', anchor=CENTER)
    viewTree.heading('Stock', text='Stock', anchor=CENTER)
    # viewTree.heading('Sold', text='Sold', anchor=CENTER)
    viewTree.heading('Stock Value', text='Stock Value', anchor=CENTER)
    viewTree.grid(row = 0,column = 0,pady=20)


