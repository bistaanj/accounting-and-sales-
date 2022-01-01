# from os import _OnError
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from datetime import datetime
from config.dynamicSize import HR, WR, FR
from Frames.supportingFunctions import getUnitCostPrice
from Frames.Inventory.features import newRow
# creates widget inside Inventory Label Frame. Tab-> Inventory


def getDateTime(self):
    nw = datetime.now(self)
    date = nw.strftime("%d/%m/%Y")
    time = nw.strftime("%H:%M")
    return (date, time)
# Gets the data from the self.displayLabel -> creates json data -> post data to cloud


def fetchRecord(self):
    self.widgetValue = []
    self.widgetlabel = []
    for widget in self.displayLabel.winfo_children():
        if(widget.winfo_class() == "TLabel"):
            self.widgetlabel.append(widget.cget("text"))
        elif (widget.winfo_class() == "Entry"):
            self.widgetValue.append(widget.get())
        elif (widget.winfo_class() == "TCombobox"):
            self.widgetValue.append(widget.get())
        elif (widget.winfo_class() == "Text"):
            self.widgetValue.append(widget.get(1.0, 'end-1c'))
        else:
            continue

    self.capturedRecord = dict(zip(self.widgetlabel, self.widgetValue))
    return self.capturedRecord


def createRecord(self, inventory):
    self.rawData = fetchRecord(self)
    try:
        for x in self.widgetValue:
            if (x == ''):
                raise ValueError
        postRecord(self, inventory)
    except ValueError:
        messagebox.showwarning("Insufficient Record", "All Fields Required")

# End of Data Processing Functions

# Database updating functions


def postRecord(self, inventory):
    self.capturedRecord = self.rawData

    
    # uncomment this line for local storage
    connection = pymongo.MongoClient("localhost", 27017)
    database = connection[self.activeDatabase]
    collection = database['inventory']

    try:
        validate = collection.find_one(
            {'Product Name': self.rawData['Product Name']}, {'_id': 1})

        if (validate != None):
            raise ValueError

        try:
            self.rawData['Quantity'] = float(self.rawData['Quantity'])
            self.rawData['Sales Price'] = float(self.rawData['Sales Price'])
            self.rawData['Cost Price'] = float('{:.2f}'.format(
                float(self.rawData['Cost Price'])/float(self.rawData['Quantity'])))
            self.rawData['Order'] = 0
            self.rawData['Sold'] = 0

            inserted = collection.insert_one(self.rawData)
            ref_id = inserted.inserted_id
            collection = database['restock']
            nw = datetime.now()
            id = nw.strftime("%d%m%Y-%H%M%S")
            ref_collection = {'_id': ref_id, 'PN': self.rawData['Product Name'],
                              id: {
                'Quantity': self.rawData['Quantity'],
                'CP': self.rawData['Cost Price']
            }}
            collection.insert_one(ref_collection)
            collection = database['presentStock']

            ref_collection = {'_id': ref_id, 'PN': self.rawData['Product Name'],
                              'Stock': [{'Quantity': self.rawData['Quantity'], 'CP':self.rawData['Cost Price']}]
                              }
            collection.insert_one(ref_collection)

            collection = database['outStock']
            ref_collection = {'_id':ref_id, 'PN': self.rawData['Product Name']}
            collection.insert_one(ref_collection)

            # connection.close()
            messagebox.showinfo("Information", "Product Addition Successful")
            addNewRecord(self, inventory)
        except ValueError:
            messagebox.showerror(
                "Value Error", "Quantity and Unit Cost must be a Number.")

    except ValueError:
        messagebox.showwarning(
            'Request Denied', 'Product with same name is available in Inventory.')
    # Frame and gui for view tab


def addNewRecord(self, inventory):
    # getDateTime(self)
    try:
        self.displayFrame.destroy()
    except:
        pass


    def validateCostPrice():
        try:
            float(productCostEntry.get())
        except:
            productCostEntry.delete(-1, "end")
        try:
            float(quantityEntry.get())
        except:
            quantityEntry.delete(-1, "end")

    def showUnitCostPrice(e=""):
        if quantityEntry.get() != "" and productCostEntry.get() != "":
            validateCostPrice()
            unitCostPrice = getUnitCostPrice(
                float(productCostEntry.get()), int(quantityEntry.get()))
            productUnitCostLabel.config(
                text="Unit Cost Price: Rs."+str(unitCostPrice))
        else:
            productUnitCostLabel.config(text="Unit Cost Price: Rs.0")

    self.productCategory = StringVar()
    self.unitType = StringVar()
    self.vatIncluded = BooleanVar()
    self.totalAmount = IntVar()

    self.displayFrame = Frame(inventory, bg='#FFFFFF')
    self.displayFrame.pack(fill="both", side="left")
    bgColor = '#FFFFFF'
    self.displayLabel = LabelFrame(self.displayFrame, text="Product Details",
                                   bg=bgColor, font=('Helvetica', int(FR*30), 'bold', 'underline'), fg="#5A63F5", border=0, labelanchor='n')
    self.displayLabel.pack(fill="both", side="top", pady=20)

    s = ttk.Style()
    s.configure('TLabel', font=('Helvetica', int(FR*12), 'bold'),
                background=bgColor, foreground='#BF0909')
    productNameLabel = ttk.Label(
        self.displayLabel, text="Product Name", style='TLabel')
    productNameLabel.grid(column=0, row=1, padx=15, sticky='w')

    productNameEntry = Entry(self.displayLabel, width=int(
        WR*50), border=0, bg='#CED7D7', font=('Helvetica', int(FR*12), 'bold'))
    productNameEntry.grid(column=1, row=1, padx= int(WR*10),
                          pady=int(HR*10), sticky="w", columnspan=3)

    quantityLabel = ttk.Label(
        self.displayLabel, text="Quantity", style='TLabel')
    quantityLabel.grid(column=0, row=2, padx= int(WR*10), pady=int(HR*10), sticky="w")

    quantityEntry = Entry(self.displayLabel, width=int(WR*10), font=('Helvetica', int(FR*12), 'bold'),
                          border=0, bg='#CED7D7')
    quantityEntry.grid(column=1, row=2, padx= int(WR*10), pady=int(HR*10), sticky="w")

    pType = ttk.Label(self.displayLabel, text='Units', style='TLabel')
    pType.grid(column=2, row=2, padx=5, pady=int(HR*10))

    PtypeCombo = ttk.Combobox(self.displayLabel, background='#CED7D7', values=[
                              'Pcs', 'Pkts', 'Liters', 'Bundle', 'Kgs', 'Meter', 'Other'], font=('Comic Sans MS', int(FR*10), 'bold'))
    PtypeCombo.grid(column=3, row=2, padx=5, pady=int(HR*10), sticky="w")

    productCostLabel = ttk.Label(
        self.displayLabel, text="Cost Price", style='TLabel')
    productCostLabel.grid(column=0, row=4,  padx= int(WR*10), pady=int(HR*10), sticky="w")

    productCostEntry = Entry(self.displayLabel, width=int(
        WR*20), border=0, bg='#CED7D7', font=('Helvetica', int(FR*12), 'bold'))
    productCostEntry.grid(column=1, row=4,  padx= int(WR*10), pady=int(HR*10), sticky="w")
    productCostEntry.bind('<KeyRelease>', showUnitCostPrice)

    productUnitCostLabel = Label(self.displayLabel, text="Unit Cost Price: Rs.0", font=(
        'Helvetica', int(FR*14), 'bold'), background=bgColor, foreground='#BF0909')
    productUnitCostLabel.grid(column=1, row=4, pady=int(HR*10), padx= int(WR*10), sticky="e")
    productSalesLabel = ttk.Label(
        self.displayLabel, text="Sales Price", style='TLabel')
    productSalesLabel.grid(column=0, row=5,  padx= int(WR*10), pady=int(HR*10), sticky="w")

    productSalesEntry = Entry(self.displayLabel, width=int(
        WR*20), border=0, bg='#CED7D7', font=('Helvetica', int(FR*12), 'bold'))
    productSalesEntry.grid(column=1, row=5,  padx= int(WR*10), pady=int(HR*10), sticky="w")

    # locationLabel = ttk.Label(
    #     self.displayLabel, text='Location', style='TLabel')
    # locationLabel.grid(column=0, row=6, padx= int(WR*10), pady=int(HR*10), sticky="w")

    # locationEntry = Entry(self.displayLabel, width = int(WR*20),border=0, bg='#CED7D7', font=('Helvetica', int(FR*12), 'bold'))
    # locationEntry.grid(column=1, row=6, padx= int(WR*10), pady=int(HR*10), sticky="w")

    productDescriptionLabel = ttk.Label(
        self.displayLabel, text="Purchased From", style='TLabel')
    productDescriptionLabel.grid(
        column=0, row=7,  padx= int(WR*10), pady=int(HR*10), sticky="w")

    productDescription = Entry(self.displayLabel, border=0, width=int(
        WR*50), bg='#CED7D7', font=('Helvetica', int(FR*12), 'bold'))
    productDescription.grid(column=1, row=7, padx= int(WR*10), pady=int(HR*10), sticky="w")

    productDescriptionLabel = Label(
        self.displayLabel, text="Alternative Measures of Sales : ", bg = "#ffffff", fg ='grey', font = ('Comic Sans MS', int(FR*15), 'bold', 'underline'))
    productDescriptionLabel.grid(
        column=0, row=8,  padx= int(WR*10), pady=int(HR*15), sticky="w", columnspan= 2)

    
    ucOuterFrame = Frame(self.displayLabel, bg = '#ffffff')
    ucOuterFrame.grid(row = 9, column= 0, rowspan= 4, columnspan= 6)
    
    ucInnerFrame = Frame(ucOuterFrame, bg = '#ffffff')
    ucInnerFrame.pack(side='top', fill='both')
    newRow.createNewRow(ucInnerFrame)

    newRow_btn = Button(ucOuterFrame, text = 'Add New Row', command = lambda:newRow.countRows(ucInnerFrame,ucOuterFrame) )
    newRow_btn.pack(side='bottom')



    # self.submit_record_btn = Button(self.displayLabel, cursor="hand2", text="Record", command=lambda: createRecord(self, inventory),
    #                                 font=('Times New Roman', int(FR*20)), bg='#648EF1', fg='#FFFFFF', border=0)
    # self.submit_record_btn.grid(column=0, row=8, padx= int(WR*10), pady=20, sticky="se")

    # tips = Label(self.displayLabel, text="*record validations:-",
    #              font=('Times New Roman', int(FR*10), 'underline'), fg='red', bg='white')
    # tips.grid(column=0, row=9, padx=5, pady=int(HR*10), sticky="w")

    # tips = Label(self.displayLabel, text="- check for the product in inventory before recording",
    #              font=('Times New Roman', int(FR*10)), fg='red', bg='white')
    # tips.grid(column=0, row=10, padx=5, pady=0, sticky="w", columnspan=2)

    # tips = Label(self.displayLabel, text="- recording of similar product will pop error msg",
    #              font=('Times New Roman', int(FR*10)), fg='red', bg='white')
    # tips.grid(column=0, row=11, padx=5, pady=0, sticky="w", columnspan=2)

    # tips = Label(self.displayLabel, text="- ensure all fields are filled before recording",
    #              font=('Times New Roman', int(FR*10)), fg='red', bg='white')
    # tips.grid(column=0, row=12, padx=5, pady=0, sticky="w", columnspan=2)

    # tips = Label(self.displayLabel, text="- 'Quantity' and 'Sales Price' must be a number",
    #              font=('Times New Roman', int(FR*10)), fg='red', bg='white')
    # tips.grid(column=0, row=13, padx=5, pady=0, sticky="w", columnspan=2)
