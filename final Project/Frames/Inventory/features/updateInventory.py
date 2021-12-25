# from _typeshed import ReadableBuffer
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from bson.objectid import ObjectId
from datetime import datetime
import pymongo
from config.dynamicSize import FR, WR, HR
from Frames.supportingFunctions import warnUser


def updateInventory(self):
    self.displayFrame.destroy()
    self.displayFrame = Frame(self.inventory, bg='#FFFFFF')
    self.displayFrame.pack(fill="both", side="left")

    self.searchFrame = Frame(self.displayFrame, bg='#4F83FC')
    self.searchFrame.pack(pady=10)  # fill ='x', side = 'left', anchor = N

    def getObjectIid():
        row_iid = viewTree.focus()
        if(row_iid == ''):
            return 0
        else:
            return row_iid

    def displayUpdatePopup(displayText, cmd):
        self.UpdatePopUp = Toplevel()
        self.UpdatePopUp.grab_set()
        self.UpdatePopUp.iconbitmap('./res/dsk.ico')
        self.UpdatePopUp.title("Update Values")

        self.UpdatePopUp.geometry("+%d+%d" % (400, 300))
        self.UpdatePopUp.minsize(250, 200)

        self.updateLabel = Label(self.UpdatePopUp, text=displayText)
        self.updateLabel.pack(padx=10, pady=10)
        self.updateEntry = Entry(self.UpdatePopUp, width=20)
        self.updateEntry.pack(padx=10, pady=10)
        self.updateEntry.focus()
        self.updateEntry.bind('<Return>', cmd)
        updateBtn = Button(self.UpdatePopUp, text="Update Value", command=cmd)
        updateBtn.pack(padx=10, pady=20)

    def displayUpdateForm():

        def getCred():
            a = quantity_entry.get()
            b = cp_entry.get()
            c = seller_entry.get()
            print(a, b, c)
            dbsQuantityUpdate(a, b, c)

        self.UpdatePopUp = Toplevel()
        self.UpdatePopUp.grab_set()
        self.UpdatePopUp.iconbitmap('./res/dsk.ico')
        self.UpdatePopUp.title("Update Quantity")

        self.UpdatePopUp.geometry("+%d+%d" % (500, 300))
        self.UpdatePopUp.minsize(350, 200)

        quantity_label = Label(self.UpdatePopUp, text=" Quantity")
        quantity_label.grid(row=0, column=0)

        quantity_entry = Entry(self.UpdatePopUp)
        quantity_entry.grid(row=0, column=1, pady=10)

        cp_label = Label(self.UpdatePopUp, text=" Cost Price")
        cp_label.grid(row=1, column=0)

        cp_entry = Entry(self.UpdatePopUp)
        cp_entry.grid(row=1, column=1, pady=10)

        seller_label = Label(self.UpdatePopUp, text=" Purchased From")
        seller_label.grid(row=2, column=0)

        seller_entry = Entry(self.UpdatePopUp, width=30)
        seller_entry.grid(row=2, column=1, pady=10, padx=5)

        # self.updateLabel = Label(self.UpdatePopUp, text=displayText)
        # self.updateLabel.pack(padx=10, pady=10)
        # self.updateEntry = Entry(self.UpdatePopUp, width=20)
        # self.updateEntry.pack(padx=10, pady=10)
        # self.updateEntry.focus()
        # self.updateEntry.bind('<Return>', cmd)
        updateBtn = Button(
            self.UpdatePopUp, text="Update Value", command=getCred)
        updateBtn.grid(row=3, column=0, pady=10)

    def dbsQuantityUpdate(quantity, cp, seller):

        try:
            iid = self.row_iid
            # grabbedValue = int(self.updateEntry.get())
            grabbedValue = quantity
            grabbedValue = int(grabbedValue)
            if (grabbedValue == '0'):
                raise ValueError

            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database('saiRecords')
            # collection = db.inventory

            # For local Storage
            connection = pymongo.MongoClient("localhost", 27017)
            database = connection['saiRecords']
            collection = database['inventory']

            databaseRow = collection.find_one(
                {'_id': ObjectId(iid)}, {'Quantity': 1, 'Product Name': 1, '_id': 0})
            # connection.close()
            currentValue = databaseRow['Quantity']
            print(type(currentValue))
            print(type(grabbedValue))

            currentValue = int(currentValue)
            newValue = grabbedValue + currentValue
            collection.update_one({'_id': ObjectId(iid)}, {
                                  '$set': {'Quantity': newValue}})
            cp = float(cp)
            quantity = int(quantity)
            cp = float('{:.2f}'.format(cp/quantity))
            collection.update_one({'_id': ObjectId(iid)}, {
                                  '$set': {'Cost Price': cp}})
            self.UpdatePopUp.destroy()
            collection = database['restock']
            nw = datetime.now()
            id = nw.strftime("%d%m%Y-%H%M%S")

            print(iid)
            rawdata = {}
            rawdata['Quantity'] = quantity
            rawdata['CP'] = cp
            rawdata['Seller'] = seller
            collection.update_one({'_id': ObjectId(iid)}, {
                                  '$set': {id: rawdata}})

            # cumi= {}
            # cumi['Quantity']= quantity
            # cumi['CP']= cp
            collection = database['presentStock']
            collection.update_one({'_id': ObjectId(iid)}, {
                                  '$push': {'Stock': {'Quantity': quantity, 'CP': cp}}})

            # for x in rawdata[::-1]:
            #     print(rawdata[x]['Seller'])

            # rawdata={
            #     '_id':123456789,
            #     "20112021-221205":{
            #             "Quantity":100,
            #             "CP":500,
            #             "Purchased From": "ABC"
            #         },
            #     "20112021-221305":{
            #             "Quantity":100,
            #             "CP":500,
            #             "Purchased From": "ABC"
            #         },

            # }

            # for x in rawdata:
            #     print(rawdata[x])

            for x in rawdata:
                print(x)
                print(rawdata[x])
            rawdata
            warnUser("Value Updated")
            displaySearchResult()
        except ValueError:
            messagebox.showerror('Error', 'Value Missing or Insufficient')
            self.UpdatePopUp.destroy()

    def dbsCostUpdate(event=''):
        try:
            iid = self.row_iid
            grabbedValue = int(self.updateEntry.get())
            if (grabbedValue == 0):
                raise ValueError

            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database('saiRecords')
            # collection = db.inventory

            # For local Storage
            connection = pymongo.MongoClient("localhost", 27017)
            database = connection['saiRecords']
            collection = database['inventory']

            collection.update_one({'_id': ObjectId(iid)}, {
                                  '$set': {'Sales Price': grabbedValue}})
            self.UpdatePopUp.destroy()
            warnUser("Value Updated")
            displaySearchResult()
        except ValueError:
            messagebox.showerror('Error', 'Value Missing or Insufficient')
            self.UpdatePopUp.destroy()
    # def dbsLocationUpdate(event = ''):
    #     try:
    #         iid = self.row_iid
    #         grabbedValue = self.updateEntry.get()
    #         if (grabbedValue == 0):
    #             raise ValueError
    #         grabbedValue = str(grabbedValue)

    #         # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    #         # db = client.get_database('saiRecords')
    #         # collection = db.inventory

    #         ##For local Storage
    #         connection = pymongo.MongoClient("localhost", 27017)
    #         database = connection['saiRecords']
    #         collection = database['inventory']

    #         collection.update_one({'_id': ObjectId(iid)}, {
    #                             '$set': {'Location': grabbedValue}})
    #         self.UpdatePopUp.destroy()
    #         warnUser("Value Updated")
    #         displaySearchResult()
    #     except ValueError:
    #         messagebox.showerror('Error', 'Value Missing or Insufficient')
    #         self.UpdatePopUp.destroy()

    def updateQuantityDbs():
        self.row_iid = getObjectIid()
        if self.row_iid == 0:
            warnUser("One Record Selection Required !")
        else:
            displayUpdateForm()

    def updateCostDbs():
        self.row_iid = getObjectIid()
        if self.row_iid == 0:
            warnUser("One Record Selection Required !")
        else:
            displayUpdatePopup("Update Value", dbsCostUpdate)

    # def updateLocationDbs():
    #     self.row_iid = getObjectIid()
    #     if self.row_iid == 0:
    #         warnUser("One Record Selection Required !")
    #     else:displayUpdatePopup("Update Value", dbsLocationUpdate)

    def displaySearchResult(event=""):
        searchResult = []
        # print("Checking Search Result")
        # print(searchResult)
        clearTree()
        searchValue = self.searchEntry.get()
        # print(searchValue)

        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.inventory

        # For Local Database
        connection = pymongo.MongoClient("localhost", 27017)
        database = connection['saiRecords']
        collection = database['inventory']
        searchResult = collection.find(
            {"Product Name": {'$regex': searchValue, '$options': 'i'}})
        searchResult2 = collection.find(
            {"Product Name": {'$regex': searchValue, '$options': 'i'}})

        # connection.close()
        showCondition = FALSE
        lenCheck = len(list(searchResult2))

        if (lenCheck == 0):
            warnUser("Product Not Found")
            print("Warned !!!!!!!")
        else:
            showCondition = True
        if (showCondition == TRUE):
            self.txt = 0
            for x in searchResult:
                viewTree.insert(parent='', index=END, iid=(x["_id"]), text=(self.txt+1), values=(
                    x['Product Name'], x['Cost Price'], x['Sales Price'], x['Quantity'], x['Units'], x['Purchased From']))
                self.txt += 1

    # searchLabel = Label(self.searchFrame, text="Product", bg='#4F83FC', fg = '#FFFFFF')
    # searchLabel.grid(column=0, row=1, padx=10, pady=10, sticky="w")

    def clearPlaceHolder(event):
        self.searchEntry.delete(0, 'end')

    def phaseOutProducts():
        try:
            iid = viewTree.focus()
            if (iid == ''):
                raise ValueError
            conformation = messagebox.askyesno(
                "Conformation Required", "This process is irreversible. Are you sure?")
            if conformation:
                # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                # db = client.get_database('saiRecords')
                # collection = db.inventory
                # For Local Database
                connection = pymongo.MongoClient("localhost", 27017)
                database = connection['saiRecords']
                collection = database['inventory']
                trans = collection.delete_one({'_id': ObjectId(iid)})
                print(trans)
                messagebox.showinfo(
                    "Transaction Completed", "Product Removed Successfully")
                connection.close()
                self.viewInventory()
        except ValueError:
            messagebox.showerror(
                "Invalid Request", "Product Selection required")

    self.searchEntry = Entry(self.searchFrame, width=int(
        WR*40), bg='#4F83FC', fg='#FFFFFF', border=0, font=('Comic Sans MS', int(FR*15)))
    self.searchEntry.grid(column=1, row=1, padx=10, pady=10, sticky="w")
    self.searchEntry.insert(0, 'search for...')
    self.searchEntry.bind('<FocusIn>', clearPlaceHolder)
    self.searchEntry.bind('<KeyRelease>', displaySearchResult)
    self.searchEntry.bind('<Return>', displaySearchResult)

    searchBtn = Button(self.searchFrame, text="GO", command=displaySearchResult,
                       font=('Times New Roman', int(FR*18), 'bold', 'underline'), bg='#4F83FC', fg='#FFFFFF', border=0, cursor="hand2")
    searchBtn.grid(column=2, row=1, padx=10, pady=10, sticky="w")

    self.rsltFrame = Frame(self.displayFrame, bg='white')
    self.rsltFrame.pack()  # fill = 'both', side = 'left', anchor = S

    lb = Label(self.rsltFrame, text='Search Result', font=(
        'Helvetica', int(FR*15), 'bold', 'underline'), bg='white')
    lb.pack(pady=20)
    # Table view starts from here
    viewTree = ttk.Treeview(self.rsltFrame, height=int(
        HR*8), style="mystyle.Treeview")

    # Define Columns
    viewTree['columns'] = ('Product Name', 'Cost Price',
                           'Sales Price', 'Quantity', 'Units')
    viewTree.column('#0', width=int(WR*60), minwidth=10, anchor=CENTER)
    viewTree.column('Product Name', width=int(WR*350), anchor=W)
    viewTree.column('Cost Price', width=int(WR*138), anchor=CENTER)
    viewTree.column('Sales Price', width=int(WR*138), anchor=CENTER)
    viewTree.column('Quantity', width=int(WR*130), anchor=CENTER)
    viewTree.column('Units', width=int(WR*110), anchor=CENTER)
    # viewTree.column('Location', width = int(WR*150), anchor=CENTER)

    # Create Headings
    viewTree.heading('#0', text='S.N', anchor=CENTER)
    viewTree.heading('Product Name', text='Product Name', anchor=W)
    viewTree.heading('Cost Price', text='Cost Price', anchor=CENTER)
    viewTree.heading('Sales Price', text='Sales Price', anchor=CENTER)
    viewTree.heading('Quantity', text='Quantity', anchor=CENTER)
    viewTree.heading('Units', text='Units', anchor=CENTER)
    # viewTree.heading('Location', text='Location', anchor=CENTER)

    viewTree.pack(padx=10)

    def clearTree():
        for rows in viewTree.get_children():
            viewTree.delete(rows)

    self.btnFrame = Frame(self.displayFrame, bg='pink')
    self.btnFrame.pack()

    addQuantity = Button(
        self.btnFrame, text='Add Quantity', command=updateQuantityDbs)
    addQuantity.grid(column=0, row=0, padx=10, pady=10, sticky="w")

    changeCost = Button(self.btnFrame, text="Update Cost",
                        command=updateCostDbs)
    changeCost.grid(column=1, row=0, padx=10, pady=10, sticky="w")

    # changeLocation = Button(
    #     self.btnFrame, text="Update Location", command=updateLocationDbs)
    # changeLocation.grid(column=2, row=0, padx=10, pady=10, sticky="w")

    phaseoutBtn = Button(
        self.btnFrame, text='Phase Out Product', command=phaseOutProducts)
    phaseoutBtn.grid(column=3, row=0, padx=10, pady=10, sticky="w")
