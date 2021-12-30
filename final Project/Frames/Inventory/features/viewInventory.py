from config.dynamicSize import FR, WR, HR
from tkinter import *
from tkinter import ttk
import pymongo
from bson.objectid import ObjectId
from Frames.supportingFunctions import warnUser

def viewInventory(self,tab):
    try:
        self.displayFrame.destroy()
    except:pass    
    self.displayFrame = Frame(tab)
    self.displayFrame.pack(fill="both", side="left")

    searchFrame = Frame(self.displayFrame)
    searchFrame.pack(fill='both', padx = 100)

    def clearPlaceHolder(event):
        self.searchEntry.delete(0, 'end')

    def clearTree():
        for rows in viewTree.get_children():
            viewTree.delete(rows)

    def displaySearchResult(event=""):
        searchResult = []
        
        clearTree()
        searchValue = self.searchEntry.get()

        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database(self.activeDatabase)
        # collection = db.inventory
        ##For local Database Storage
        connection = pymongo.MongoClient("localhost", 27017)
        database = connection[self.activeDatabase]
        collection = database['inventory']
        searchResult = collection.find(
            {"Product Name": {'$regex': searchValue, '$options': 'i'}})
        searchResult2 = collection.find(
            {"Product Name": {'$regex': searchValue, '$options': 'i'}})
        connection.close()
        showCondition = FALSE
        lenCheck = len(list(searchResult2))
        if (len(searchValue) == 0):
            viewTree.pack_configure(expand=1)
            totslOrderLabel.pack_forget()
            totalSoldLabel.pack_forget()
        else:
            viewTree.pack_configure(expand=0)
            
        if (lenCheck == 0):
            warnUser("Product Not Found")
        else:
            showCondition = True
        if (showCondition == TRUE):
            self.txt = 0
            for x in searchResult:
                viewTree.insert(parent='', index=END, iid=(x["_id"]), text=(self.txt+1), values=(
                    x['Product Name'], x['Cost Price'], x['Sales Price'], x['Quantity'], x['Units'], x['Purchased From']))
                self.txt += 1
    

    totalSoldLabel = Label(self.displayFrame,text="",font=('Comic Sans MS', int(FR*15)))
    totslOrderLabel = Label(self.displayFrame,text="",font=('Comic Sans MS', int(FR*15)))
    
    self.searchEntry = Entry(searchFrame, width = int(WR*40), bg='#4F83FC', fg='#FFFFFF',border=0, font=('Comic Sans MS', int(FR*20)))
    self.searchEntry.grid(column=1, row=1, padx=10, pady=10, sticky="w")
    self.searchEntry.insert(0,'search for...')
    self.searchEntry.bind('<FocusIn>', clearPlaceHolder)
    self.searchEntry.bind('<KeyRelease>', displaySearchResult)
    self.searchEntry.bind('<Return>',displaySearchResult)

    searchBtn=Button(searchFrame, text = "GO", command = displaySearchResult,
    font=('Times New Roman', int(FR*18),'bold','underline'), bg='#4F83FC', fg = '#FFFFFF',border = 0, cursor = "hand2")
    searchBtn.grid(column=2, row=1, padx=10, pady=10, sticky="w")


    viewTree = ttk.Treeview(self.displayFrame,  style="mystyle.Treeview")

    #Define Columns
    viewTree['columns'] = ('Product Name', 'Cost Price',
                            'Sales Price', 'Quantity', 'Units', 'Purchased From')
    viewTree.column('#0', width = int(WR*60), minwidth=10, anchor=CENTER)
    viewTree.column('Product Name', width = int(WR*200), anchor=W)
    viewTree.column('Cost Price', width = int(WR*138), anchor=CENTER)
    viewTree.column('Sales Price', width = int(WR*138), anchor=CENTER)
    viewTree.column('Quantity', width = int(WR*130), anchor=CENTER)
    viewTree.column('Units', width = int(WR*110), anchor=CENTER)
    # viewTree.column('Location', width = int(WR*150), anchor=CENTER)
    viewTree.column('Purchased From', width = int(WR*150), anchor=CENTER)

    #Create Headings
    viewTree.heading('#0', text='S.N', anchor=CENTER)
    viewTree.heading('Product Name', text='Product Name', anchor=W)
    viewTree.heading('Cost Price', text='Cost Price', anchor=CENTER)
    viewTree.heading('Sales Price', text='Sales Price', anchor=CENTER)
    viewTree.heading('Quantity', text='Quantity', anchor=CENTER)
    viewTree.heading('Units', text='Units', anchor=CENTER)
    # viewTree.heading('Location', text='Location', anchor=CENTER)
    viewTree.heading('Purchased From', text='Purchased', anchor=CENTER)
    viewTree.pack(fill = 'both',expand = 1, padx = 20,pady = 20)
    self.viewTree = viewTree
    
    def showDetailsOfProduct(event=''):
        row_iid = viewTree.focus()
        if(row_iid != ''):
            viewTree.pack_configure(expand=0)
            connection = pymongo.MongoClient("localhost", 27017)
            database = connection[self.activeDatabase]
            collection = database['inventory']
            databaseRow = collection.find_one({'_id': ObjectId(row_iid)})
            totalSoldLabel.pack()
            totslOrderLabel.pack()
            totalSoldLabel.config(text='Items sold: '+ str(databaseRow['Sold']))
            totslOrderLabel.config(text='Items Ordered: '+ str(databaseRow['Order']))
        else:
            viewTree.pack_configure(expand=1)
            totslOrderLabel.pack_forget()
            totalSoldLabel.pack_forget()


    viewTree.bind('<ButtonRelease-1>',showDetailsOfProduct)
    

    # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # db = client.get_database(self.activeDatabase)
    # collection = db.inventory
    ##For local database Storage
    connection = pymongo.MongoClient("localhost", 27017)
    database = connection[self.activeDatabase]
    collection = database['inventory']

    inventorydata= collection.find()

    self.txt=0
    for x in inventorydata:
        qnty = x['Quantity']
        if (qnty== 0):
            qnty = "Out of Stock"
        viewTree.insert(parent='', index=END , iid=(x["_id"]), text =(self.txt+1), values =(x['Product Name'],x['Cost Price'], x['Sales Price'], qnty,x['Units'],x['Purchased From']))
        self.txt+=1
    self.btnFrame = Frame(self.displayFrame, bg='pink')
    self.btnFrame.pack()
    connection.close()
