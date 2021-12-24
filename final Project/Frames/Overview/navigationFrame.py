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
    def insertDate(e=""):
        today = datetime.date(datetime.now())
        chooseEndDate.set_date(today)
    
    def insertInTable(listForTable):
        count = 0
        for rows in viewTree.get_children():
            viewTree.delete(rows)

        for values in listForTable:
            viewTree.insert(parent='', index=END,iid=(values["_id"]),
                        text=(count+1),
                        values=(
                    values["Product Name"],
                    values['Cost Price'],
                    values['Current Stock'],
                    values['Stock'],
                    # values['Sold'],
                    values['Stock Value']
                    ))
            count+=1

    def getDateAndShowToTable():
        descriptionLabel.config(text="The stock of products in your shop at " + chooseEndDate.get() +"  is:")
        endDate = chooseEndDate.get_date()
        if endDate > datetime.date(datetime.now()) :
            warnUser("invalid Date Provided")
        else:
            collection1 = getConnect('saiRecords',"restock")
            collection2 = getConnect('saiRecords',"inventory")
            result = collection1.find()
            totalStockValue =0
            listForTable = []
            for i in result:
                rawData = {}
                stock = 0
                stockValue = 0
                TS = 0    #total stock
                for key in list(i):
                    if key != "_id":
                        TS+=int(i[key]["Quantity"])
                        d = datetime.date(datetime.strptime(key[0:8],'%d%m%Y'))
                        if(d <= endDate):
                            iid = i[key]["Product"]
                            stock+=int(i[key]["Quantity"])
                            product = collection2.find_one({"_id":ObjectId(iid)})
                            rawData["_id"] = product["_id"]
                            rawData["Product Name"] = product["Product Name"]
                            rawData["Current Stock"] = product["Quantity"]
                            rawData["Cost Price"]  = product["Cost Price"]
                            rawData["Sold"] = product["Sold"]
                            stockValue+= float(i[key]["CP"])
                if rawData:
                    rawData["Stock"] = stock
                    rawData["Stock Value"] = stockValue
                    listForTable.append(rawData)
                totalStockValue+=stockValue

            removeDetailsTable()
            insertInTable(listForTable)
            totalStockValueLabel.config(text="Toal Stock Value =  Rs. "+str(totalStockValue))

    def showDetails(e=""):
        iid = viewTree.focus()
        if iid != "":
            count = 0
            detailsOfStockLabel.grid(row=1,column=1,rowspan=2)
            detailsTable.grid(row = 2,column = 1,pady=20,rowspan=7)
            endDate = chooseEndDate.get_date()
            collection = getConnect("saiRecords","restock")
            detailsToShow = []
            # result  = collection.find_one({"_id":ObjectId(iid)})
            temp = collection.find()
            for i in temp:
                for key in list(i):
                    if key != "_id":
                        d = datetime.date(datetime.strptime(key[0:8],'%d%m%Y'))
                        if (d <= endDate) and i[key]["Product"] == str(iid):
                            rawData = {}
                            rawData["Date"] = d
                            rawData["Cost Price"] = i[key]["CP"]
                            rawData["Quantity"] = i[key]["Quantity"]
                            detailsToShow.append(rawData)

            # for key in list(result):
            #     if key != "_id":
            #         d = datetime.date(datetime.strptime(key[0:8],'%d%m%Y'))
            #         if (d <= endDate):
            #             rawData = {}
            #             rawData["Date"] = d
            #             rawData["Cost Price"] = result[key]["CP"]
            #             rawData["Quantity"] = result[key]["Quantity"]
            #             detailsToShow.append(rawData)

            for rows in detailsTable.get_children():
                detailsTable.delete(rows)

            for values in detailsToShow:
                detailsTable.insert(parent='', index=END,
                            text=(count+1),
                            values=(
                        values["Date"],
                        values['Cost Price'],
                        values['Quantity']
                        ))
                count+=1
        else:
            removeDetailsTable()
            # detailsOfStockLabel.grid_forget()
            # detailsTable.grid_forget()
            

    def removeDetailsTable(e=""):
        # print("sth")
        detailsTable.grid_forget()
        detailsOfStockLabel.grid_forget()
        # removeTableButton.grid_forget()
        

    self.displayFrame = Frame(tab)
    self.displayFrame.pack(fill = 'both')

    descLabel = Label(self.displayFrame,text="Overview of Stocks",font=(fontToUse,int(FR*20)))
    descLabel.pack()
    topFrame = Frame(self.displayFrame)
    topFrame.pack()
    
    fromLabel = Label(topFrame,text="Search Stock at ",font=(fontToUse,int(FR*10)))
    fromLabel.grid(row =  0 ,column= 0,padx=5)

    chooseEndDate = DateEntry(topFrame,width=12, background='darkblue',selectmode='day',
                    foreground='white', borderwidth=2, year=2021)
    chooseEndDate.grid(row = 0,column = 1,padx= 5)

    todayDateButton = Button(topFrame,text="today",command=insertDate)
    todayDateButton.grid(row=1,column=1)

    findButton = Button (topFrame,text = "Find",font = (fontToUse,int(FR*11)),command=getDateAndShowToTable)
    findButton.grid(row = 0,column = 3,padx=5)
    
    # GuI for overView Table 

    # detailsFrame = Frame(self.displayFrame)
    # detailsFrame.pack()

    deleteImage = PhotoImage(file = "./res/delete.png")


    descriptionLabel = Label(topFrame,text="The stock of products in your shop at  " + chooseEndDate.get() +"  is :",font= (fontToUse,int(FR*15)))
    descriptionLabel.grid(columnspan=5,pady=12)


    tableFrame = Frame(self.displayFrame)
    tableFrame.pack(padx = 20)
    
    stockAndStockValueLabel = Label(tableFrame,text="Stock and Stock Value at particular date frame",font=(fontToUse,int(FR*12)))
    detailsOfStockLabel = Label(tableFrame,text="details of stock",font=(fontToUse,int(FR*12)))
    stockAndStockValueLabel.grid(row=0)
    viewTree = ttk.Treeview(tableFrame, height = int(HR*10), style="mystyle.Treeview")
    #Define Columns
    viewTree['columns']= ('Product Name','Cost Price','Current Stock', 'Stock','Stock Value')
    viewTree.column('#0', width = int(WR*50), minwidth = int(WR*40), anchor = CENTER)
    viewTree.column('Product Name', width = int(WR*180),minwidth= int(WR*160), anchor = 'w')
    viewTree.column('Cost Price', width = int(WR*170),minwidth = int(WR*130), anchor=CENTER)
    viewTree.column('Current Stock', width = int(WR*130),minwidth = int(WR*120), anchor = CENTER)
    viewTree.column('Stock', width = int(WR*80),minwidth=int(WR*60), anchor = CENTER)
    # viewTree.column('Sold', width = int(WR*80),minwidth=int(WR*60), anchor=CENTER)
    viewTree.column('Stock Value', width = int(WR*200),minwidth=int(WR*180), anchor=CENTER)

    #Create Headings
    viewTree.heading('#0',text='S.N', anchor = CENTER)
    viewTree.heading('Product Name', text='Product Name',anchor = CENTER)
    viewTree.heading('Cost Price', text='Unit Cost Price', anchor=CENTER)
    viewTree.heading('Current Stock', text='Current Stock', anchor=CENTER)
    viewTree.heading('Stock', text='Stock', anchor=CENTER)
    # viewTree.heading('Sold', text='Sold', anchor=CENTER)
    viewTree.heading('Stock Value', text='Stock Value', anchor=CENTER)
    viewTree.grid(row = 1,column = 0,pady=20,rowspan=10)

    viewTree.bind('<ButtonRelease-1>',showDetails)

    detailsTable = ttk.Treeview(tableFrame, height = int(HR*7), style="mystyle.Treeview")
    #Define Columns
    detailsTable['columns']= ('Date','Cost Price','Quantity')
    detailsTable.column('#0', width = int(WR*50), minwidth = int(WR*40), anchor = CENTER)
    detailsTable.column('Date', width = int(WR*150),minwidth= int(WR*130), anchor = 'w')
    detailsTable.column('Cost Price', width = int(WR*130),minwidth = int(WR*100), anchor=CENTER)
    detailsTable.column('Quantity', width = int(WR*130),minwidth = int(WR*120), anchor = CENTER)
    #Create Headings
    detailsTable.heading('#0',text='S.N', anchor = CENTER)
    detailsTable.heading('Date', text='Date',anchor = CENTER)
    detailsTable.heading('Cost Price', text='Cost Price', anchor=CENTER)
    detailsTable.heading('Quantity', text='Quantity', anchor=CENTER)
    
    bottomFrame = Frame(self.displayFrame)
    bottomFrame.pack()

    totalStockValueLabel = Label(bottomFrame,text="Toal Stock Value =  Rs. 0.00",font=(fontToUse,int(FR*15)))
    totalStockValueLabel.pack()
