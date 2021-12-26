from tkinter import ttk
from bson.objectid import ObjectId
from config.dynamicSize import WR, FR, HR, fontToUse, day1Date
from Frames.supportingFunctions import warnUser
from Frames.getConnect import getConnect

from tkinter import *
from tkcalendar import DateEntry
from datetime import datetime

# Current date time in local system


def navigationFrame(self, tab):
    def insertDate(e=""):
        today = datetime.date(datetime.now())
        chooseEndDate.set_date(today)

    def insertInTable(listForTable):
        totalStockValue = 0
        count = 0
        for rows in viewTree.get_children():
            viewTree.delete(rows)

        for values in listForTable:
            viewTree.insert(parent='', index=END, iid=(values["_id"]),
                            text=(count+1),
                            values=(
                values["Product Name"],
                values['Cost Price'],
                values['Current Stock'],
                values['Stock'],
                # values['Sold'],
                values['Stock Value']
            ))
            totalStockValue += float(values['Stock Value'])
            count += 1
        totalStockValueLabel.config(
            text="Toal Stock Value =  Rs. "+str("{:.2f}".format(float(totalStockValue))))

    def getDateAndShowToTable():
        for rows in detailsTable.get_children():
                detailsTable.delete(rows)            
        descriptionLabel.config(
            text="The stock at the end of " + chooseEndDate.get() + "  is:")
        endDate = chooseEndDate.get_date()
        
        if endDate > datetime.date(datetime.now()):
            warnUser("invalid Date Provided")
        else:
            collection1 = getConnect('saiRecords', "restock")
            collection2 = getConnect('saiRecords', "inventory")
            collection3 = getConnect('saiRecords', "outStock")
            result = collection1.find()
            listForTable = []
            for i in result:
                rawData = {}
                stock = 0
                stockValue = 0
                TS = 0  # total stock
                iid = i['_id']
                for key in i:
                    if key != "_id" and key != "PN":
                        TS += int(i[key]["Quantity"])
                        d = datetime.date(
                            datetime.strptime(key[0:8], '%d%m%Y'))
                        if(d <= endDate):
                            # iid = i["_id"]
                            stock += int(i[key]["Quantity"])
                            product = collection2.find_one(
                                {"_id": ObjectId(iid)})
                            rawData["_id"] = product["_id"]
                            rawData["Product Name"] = product["Product Name"]
                            rawData["Current Stock"] = product["Quantity"]
                            rawData["Cost Price"] = product["Cost Price"]
                            rawData["Sold"] = product["Sold"]
                            stockValue += float(i[key]["CP"]) * \
                                int(i[key]["Quantity"])

                saleAtTime = collection3.find_one({"_id": ObjectId(iid)})
                soldQty = 0
                soldStockValue = 0
                for k in saleAtTime:
                    if k != "_id" and k != "PN":
                        d = datetime.date(
                            datetime.strptime(k[0:8], '%d%m%Y'))
                        if d <= endDate:
                            for x in saleAtTime[k]:
                                soldQty += int(x['Quantity'])
                                soldStockValue += int(x['Quantity']) * \
                                    float(x["CP"])

                if rawData:
                    rawData["Stock"] = stock - soldQty
                    rawData["Stock Value"] = stockValue - soldStockValue
                    listForTable.append(rawData)

            insertInTable(listForTable)

    def showDetails(e=""):
        iid = viewTree.focus()
        if iid != "":
            count = 0
            endDate = chooseEndDate.get_date()
            collection1 = getConnect("saiRecords", "restock")
            collection2 = getConnect("saiRecords", "outStock")
            detailsToShow = []
            result1 = collection1.find_one({"_id": ObjectId(iid)})
            result2 = collection2.find_one({"_id": ObjectId(iid)})

            for key1 in result1:
                if key1 != "_id" and key1 != "PN":
                    d = datetime.date(datetime.strptime(key1[0:8], '%d%m%Y'))
                    if (d <= endDate):
                        rawData = {}
                        rawData["Date"] = d
                        rawData["Cost Price"] = result1[key1]["CP"]
                        rawData["Quantity"] = int(result1[key1]['Quantity'])
                        detailsToShow.append(rawData)

            soldStock = {}
            for key2 in list(result2):
                if key2 != "_id" and key2 != "PN":
                    d1 = datetime.date(datetime.strptime(key2[0:8], '%d%m%Y'))
                    if d1 <= endDate:
                        for i in result2[key2]:
                            try:
                                soldStock[i['CP']]["sold"] = int(
                                    soldStock[i['CP']]["sold"]) + int(i['Quantity'])
                            except:
                                soldStock[i['CP']] = {"sold": int(
                                    i['Quantity']), "done": False}
            for values in reversed(detailsToShow):
                for i in soldStock:
                    if values["Cost Price"] == i and not soldStock[i]["done"]:
                        soldStock[i]["done"] = True
                        values["Quantity"] = int(
                            values["Quantity"]) - int(soldStock[i]['sold'])
                        if int(values["Quantity"]) == 0:
                            detailsToShow.remove(values)

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
                count += 1

    self.displayFrame = Frame(tab)
    self.displayFrame.pack(fill='both')

    descLabel = Label(self.displayFrame,
                      text="Overview of Stocks", font=(fontToUse, int(FR*20)))
    descLabel.pack()
    topFrame = Frame(self.displayFrame)
    topFrame.pack(side = 'top')
    bottomFrame = Frame(self.displayFrame)
    bottomFrame.pack(side = 'bottom', pady = WR*20)

    fromLabel = Label(topFrame, text="Search Stock at ",
                      font=(fontToUse, int(FR*10)))
    fromLabel.grid(row=0, column=0, padx=5)

    chooseEndDate = DateEntry(topFrame, width=12, background='darkblue', selectmode='day',
                              foreground='white', borderwidth=2, year=2021)
    chooseEndDate.grid(row=0, column=1, padx=5)

    todayDateButton = Button(topFrame, text="today", command=insertDate)
    todayDateButton.grid(row=1, column=1)

    findButton = Button(topFrame, text="Find", font=(
        fontToUse, int(FR*11)), command=getDateAndShowToTable)
    findButton.grid(row=0, column=3, padx=5)

    # GuI for overView Table

    # detailsFrame = Frame(self.displayFrame)
    # detailsFrame.pack()

    deleteImage = PhotoImage(file="./res/delete.png")

    descriptionLabel = Label(topFrame, text="The stock of products in your shop at  " +
                             chooseEndDate.get() + "  is :", font=(fontToUse, int(FR*15)))
    descriptionLabel.grid(columnspan=5, pady=12)

    tableFrame = Frame(self.displayFrame)
    tableFrame.pack(padx=WR*10, side = 'left')
    detailsFrame = Frame(self.displayFrame)
    detailsFrame.pack(padx=WR*10, side = 'left')
    

    stockAndStockValueLabel = Label(
        tableFrame, text="Stock and Stock Value at particular date frame", font=(fontToUse, int(FR*12)))
    detailsOfStockLabel = Label(
        detailsFrame, text="details of stock", font=(fontToUse, int(FR*12)))
    detailsOfStockLabel.grid(row=0, column=0)

    stockAndStockValueLabel.grid(row=0)
    viewTree = ttk.Treeview(tableFrame, height=int(
        HR*10), style="mystyle.Treeview")
    # Define Columns
    viewTree['columns'] = ('Product Name', 'Cost Price',
                           'Current Stock', 'Stock', 'Stock Value')
    viewTree.column('#0', width=int(WR*50), minwidth=int(WR*40), anchor=CENTER)
    viewTree.column('Product Name', width=int(WR*180),
                    minwidth=int(WR*160), anchor='w')
    viewTree.column('Cost Price', width=int(WR*170),
                    minwidth=int(WR*130), anchor=CENTER)
    viewTree.column('Current Stock', width=int(WR*130),
                    minwidth=int(WR*120), anchor=CENTER)
    viewTree.column('Stock', width=int(WR*80),
                    minwidth=int(WR*60), anchor=CENTER)
    # viewTree.column('Sold', width = int(WR*80),minwidth=int(WR*60), anchor=CENTER)
    viewTree.column('Stock Value', width=int(WR*200),
                    minwidth=int(WR*180), anchor=CENTER)

    # Create Headings
    viewTree.heading('#0', text='S.N', anchor=CENTER)
    viewTree.heading('Product Name', text='Product Name', anchor=CENTER)
    viewTree.heading('Cost Price', text='Unit Cost Price', anchor=CENTER)
    viewTree.heading('Current Stock', text='Current Stock', anchor=CENTER)
    viewTree.heading('Stock', text='Stock', anchor=CENTER)
    # viewTree.heading('Sold', text='Sold', anchor=CENTER)
    viewTree.heading('Stock Value', text='Stock Value', anchor=CENTER)
    viewTree.grid(row=1, column=0, pady=WR*20, rowspan=10, padx=WR*10)

    viewTree.bind('<ButtonRelease-1>', showDetails)

    detailsTable = ttk.Treeview(
        detailsFrame, height=int(HR*7), style="mystyle.Treeview")
    # Define Columns
    detailsTable['columns'] = ('Date', 'Cost Price', 'Quantity')
    detailsTable.column('#0', width=int(
        WR*50), minwidth=int(WR*40), anchor=CENTER)
    detailsTable.column('Date', width=int(WR*120),
                        minwidth=int(WR*130), anchor='w')
    detailsTable.column('Cost Price', width=int(WR*150),
                        minwidth=int(WR*100), anchor=CENTER)
    detailsTable.column('Quantity', width=int(WR*130),
                        minwidth=int(WR*120), anchor=CENTER)
    # Create Headings
    detailsTable.heading('#0', text='S.N', anchor=CENTER)
    detailsTable.heading('Date', text='Date', anchor=CENTER)
    detailsTable.heading('Cost Price', text='Unit Cost Price', anchor=CENTER)
    detailsTable.heading('Quantity', text='Quantity', anchor=CENTER)
    detailsTable.grid(row=1, column=0, pady=20, rowspan=7)

    

    totalStockValueLabel = Label(
        bottomFrame, text="Toal Stock Value =  Rs. 0.00", font=(fontToUse, int(FR*15)))
    totalStockValueLabel.pack()
