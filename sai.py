from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import json
from typing import Collection
import win32api
# from firebase import firebase
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import tkinter.font as font
import smtplib
import os
from tkinter import filedialog
from PIL import ImageTk, Image
from reportlab.pdfgen import canvas
import webbrowser as wb
import subprocess
from win32api import GetSystemMetrics, WinExec

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
WR = width/1366
HR = height/768
FR = (width*height)/(1366*768)

# Main Class
class Window(Tk):
    #The __init__ function
    def __init__(self):
        super(Window,self).__init__()
        self.title("Inventory and sales")
        self.iconbitmap('./res/dsk.ico')
        self.geometry('1366x768+0+0')
        # self.maxsize(w,h)
        self.minsize(1366,768)
        # self.maxsize(850,530)
        self.state('zoomed')

        # Creates Notebook
        tab_control = ttk.Notebook(self)
        notebookstyle = ttk.Style()
        notebookstyle.configure('TNotebook.Tab',font=('URW Gothic L', int(FR*15), 'bold'), padding=[10, 10])
        self.billingTotalAmount = 0
        self.productsInBill = {}

        #Creates Expense Tab
        self.inventory = Frame(tab_control, padx = 5, bg = "white" )
        tab_control.add(self.inventory, text ="Inventory")

        #Creates Sales Tab
        self.billingTab = ttk.Frame(tab_control)
        tab_control.add(self.billingTab, text = "Billing")

        #Creates View Tab
        self.viewTab = ttk.Frame(tab_control)
        tab_control.add(self.viewTab, text = "Bill History")

        self.settingsTab = ttk.Frame(tab_control)
        tab_control.add(self.settingsTab, text="App Settings")

        self.customerTab = ttk.Frame(tab_control)
        tab_control.add(self.customerTab, text="Customer Details")
 

        #Packs the Created Tabs in the Frame
        tab_control.pack(expand = 1, fill = "both")

        #Creates Frame for Navigation Button
        self.navigationFrame_inventory(self.inventory)
        
        #Creates Frame for Billing Tab
        self.navigationFrame_billing(self.billingTab)

        #Creates frame for view Button
        self.navigationFrame_view(self.viewTab)

        #Creates Frame for Settings Tab
        self.navigationFrame_settings(self.settingsTab)

        #Creates Frame for Customer Details
        self.navigationFrame_customerDetails(self.customerTab)



        #Creates an Empty Frame to initialize the self.displayFrame
        self.displayFrame = Frame(self.inventory)
        self.displayFrame.pack(fill = "both", side = "left")

        #Style Section for the widgets
        self.myFont = font.Font(family='Helvetica', size=int(FR*20), weight='bold')

        #Displays Inventory Page Initiallt
        self.addNewRecord()


    


    ## GUI part Starts here
    # creates frame and buttons inside the Inventory tab's Navigation Button

    def warnUser(self,text):
        messagebox.showinfo("Warning",text)

    def getConnect(self):
        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.inventory
        connection = pymongo.MongoClient('localhost',27017)
        database = connection['saiRecords']
        collection = database['inventory']
        return collection


    def navigationFrame_inventory(self,tab):

        
        buttonBg = "#284F9B"
        self.buttonFrame = Frame(tab, bg=buttonBg)
        self.buttonFrame.pack(fill = Y, side = "left" )
        
        self.belowFrame = Frame(tab, bg="#d1eded")
        self.belowFrame.pack(fill=X, side="bottom")

        s_btn = ttk.Style()
        s_btn.configure('TButton', height = int(HR*3), width = int(WR*20),border=0,
         background=buttonBg,
         font=("Helvetica",int(FR*14),'bold'))
        s_btn.map('TButton',
              foreground=[('disabled', 'yellow'),
                          ('pressed', 'red'),
                          ('active', '#5A63F5')],
              background=[('disabled', 'magenta'),
                          ('pressed', '!focus', 'cyan'),
                          ('active', 'green')],
              
              )

        self.btn_addProduct = ttk.Button(self.buttonFrame, text = "Add New Product",style ='TButton', command = self.addNewRecord)
        self.btn_addProduct.grid(column = 0 , row = 1, pady = 10)

        self.btn_update = ttk.Button(self.buttonFrame, text="Update Inventory", style='TButton', command=self.updateInventory)
        self.btn_update.grid(column=0, row=2, pady=5)

        self.btn_viewInventory = ttk.Button(
            self.buttonFrame, text="View Inventory", style='TButton', command=self.viewInventory)
        self.btn_viewInventory.grid(column=0, row=3, pady=5)

        self.btn_viewInventory = ttk.Button(
            self.buttonFrame, text="View Orders", style='TButton', command=self.viewOrders)
        self.btn_viewInventory.grid(column=0, row=4, pady=5)

        
        backupBtn = ttk.Button(
            self.buttonFrame, text="Back-up and Recovery", style='TButton', command=self.backupAndRecovery)
        backupBtn.grid(column=0, row=5, pady=5)

        backupBtn = ttk.Button(self.buttonFrame, text="Day End", style='TButton', command=self.dayEnd)
        backupBtn.grid(column=0, row=6, pady=5)

        def endSession():
            ans = messagebox.askyesno("Quit"," Any unsaved billing process will not be Saved. Are you sure ?")
            if (ans):
                self.destroy()

        quitbtn = ttk.Button(self.buttonFrame, text="Quit", style='TButton', command=endSession)
        quitbtn.grid(column=0, row=6, pady=20)


    def backupAndRecovery(self):
        self.displayFrame.destroy()
        self.displayFrame = Frame(self.inventory, bg='#FFFFFF')
        self.displayFrame.pack(fill = "both", side = "left")

        #Function to backup Database
        def backupDatabase():
            nw=datetime.now()
            date = nw.strftime("%d-%m-%Y")
            time = nw.strftime("%H-%M")

            validate = messagebox.askyesno('Backup Request', "Do you want to initiate backup process?")
            if (validate):
                top = Toplevel()
                top.grab_set()
                lbl = Label(top, text = " Backing up Database. Do not close the program ")
                lbl.pack()
                top.geometry("+%d+%d" % (400, 300))

                # Backs up in D drive by default
                command = 'mongodump --db saiRecords --host localhost:27017 --out E:/databaseBackupSI/'+str(date)+'_'+str(time)
                subprocess.call(command,shell=True)
                # os.system(command)
                top.destroy()
                messagebox.showinfo("Request Completed","Database Backup created Successfully")
        #Function to Restore database 
        def restoreDatabase():
            filename =  filedialog.askdirectory(initialdir = '/d',
            title = "Select backup File")
            command = "mongorestore --db saiRecords --dir " + str(filename)
            subprocess.call(command,shell=True)
            # os.system(command) 
            messagebox.showinfo("Restore Complete","Database Restored Successfully")
            


        backup_btn = ttk.Button(self.displayFrame, text= 'Back-up Database', command=backupDatabase)
        backup_btn.pack(padx = 50,pady=20, anchor = 'e')
        tips = Label (self.displayFrame, text = '(Use this option to back-up database)')
        tips.pack(padx = 20)

        backup_btn = ttk.Button(self.displayFrame, text='Recover Database', command=restoreDatabase)
        backup_btn.pack(padx=50, pady=20, anchor='e')
        tips = Label(self.displayFrame,
        text='(Use this option to recover database)')
        tips.pack(padx=20)


    def dayEnd(self):
        try:
            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database('saiRecords')
            # collection = db.configuration
            ##for local database
            connection = pymongo.MongoClient('localhost',27017)
            dbs = connection['saiRecords']
            collection = dbs['configuration']
            sysData=collection.find_one({'_id': 'settingsData'})
            # collection = db.dailySalesData
            collection = dbs['dilySalesData']

            dateTime = self.getDateTime()
            dte = dateTime[0]
            time = dateTime[1]
            data = collection.find_one({'_id':dte})
            if data == None:
                raise ValueError
            amount = data['daySales']
            connection.close()
            validate = bool(0)
            validate=messagebox.askyesno('Conformation Required', 'Do you want to send the data?')
            if(validate):
                sender_email = sysData['sender_email']
                receiver_email = sysData['receiver_email']
                password = sysData['sender_password']
                subject = "Total sales for " + dte
                body = f' Kaligandaki Hardware \n Day Total Sales\n Date: {dte} \n Day End Time: {time} \n\n Daily Sales Amount for today is : {amount}'
                message = f'Subject: {subject}\n\n{body}'
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
        except ValueError:
            messagebox.showerror("Invalid Request","No Sales Made Yet.")
            
        
        
    #creates widget inside Inventory Label Frame. Tab-> Inventory
    def addNewRecord(self):
        self.getDateTime()

        self.displayFrame.destroy()
        self.productCategory = StringVar()
        self.unitType = StringVar()
        self.vatIncluded = BooleanVar()
        self.totalAmount = IntVar()

        self.displayFrame = Frame(self.inventory, bg='#FFFFFF')
        self.displayFrame.pack(fill = "both", side = "left")
        bgColor = '#FFFFFF'
        self.displayLabel = LabelFrame(self.displayFrame, text="Product Details",
         bg=bgColor, font=('Helvetica',int(FR*30),'bold','underline'),fg ="#5A63F5", border=0, labelanchor = 'n' )
        self.displayLabel.pack(fill = "both", side = "top",pady = 20)

        s=ttk.Style()
        s.configure('TLabel', font=('Helvetica', int(FR*18), 'bold'),background=bgColor, foreground='#BF0909')
        productNameLabel = ttk.Label(self.displayLabel, text="Product Name", style ='TLabel' )
        productNameLabel.grid(column = 0, row = 1, padx = 15, sticky = 'w')

        productNameEntry = Entry(self.displayLabel, width = int(WR*50), border=0, bg='#CED7D7', font=('Helvetica',int(FR*15),'bold'))
        productNameEntry.grid(column = 1, row = 1, padx = 10, pady = 10, sticky = "w", columnspan= 3 )

        quantityLabel = ttk.Label(self.displayLabel, text="Quantity", style='TLabel')
        quantityLabel.grid(column = 0, row = 2, padx = 10, pady = 10, sticky = "w")

        quantityEntry = Entry(self.displayLabel, width = int(WR*10), font=('Helvetica',int(FR*15),'bold'),
                              border=0, bg='#CED7D7')
        quantityEntry.grid( column = 1, row = 2,padx = 10, pady = 10, sticky = "w")

        pType = ttk.Label(self.displayLabel, text = 'Units',style='TLabel')
        pType.grid(column=2, row=2, padx=5, pady=10)

        PtypeCombo = ttk.Combobox(self.displayLabel, background='#CED7D7', values=['Pcs','Pkts','Liters', 'Bundle','Kgs','Meter','Other'],font=('Comic Sans MS',int(FR*10),'bold'))
        PtypeCombo.grid(column = 3, row = 2, padx = 5, pady = 10, sticky = "w")

        productCostLabel = ttk.Label(
            self.displayLabel, text="Cost Price", style='TLabel')
        productCostLabel.grid(column = 0, row = 4,  padx = 10, pady = 10, sticky = "w")

        productCostEntry = Entry(self.displayLabel, width = int(WR*20), border=0, bg='#CED7D7', font=('Helvetica', int(FR*15), 'bold'))
        productCostEntry.grid(column = 1, row = 4,  padx = 10, pady = 10, sticky = "w")

        productSalesLabel = ttk.Label(
            self.displayLabel, text="Sales Price", style='TLabel')
        productSalesLabel.grid(column = 0, row = 5,  padx = 10, pady = 10, sticky = "w")

        productCostEntry = Entry(self.displayLabel, width = int(WR*20), border=0, bg='#CED7D7', font=('Helvetica', int(FR*15), 'bold'))
        productCostEntry.grid(column = 1, row = 5,  padx = 10, pady = 10, sticky = "w")

        locationLabel = ttk.Label(
            self.displayLabel, text='Location', style='TLabel')
        locationLabel.grid(column=0, row=6, padx=10, pady=10, sticky="w")

        locationEntry = Entry(self.displayLabel, width = int(WR*20),border=0, bg='#CED7D7', font=('Helvetica', int(FR*15), 'bold'))
        locationEntry.grid(column=1, row=6, padx=10, pady=10, sticky="w")

        productDescriptionLabel = ttk.Label(self.displayLabel, text="Purchased From", style='TLabel')
        productDescriptionLabel.grid(column = 0, row = 7,  padx = 10, pady = 10, sticky = "w")

        productDescription = Entry(self.displayLabel, border = 0,width = int(WR*50),bg='#CED7D7', font=('Helvetica',int(FR*15),'bold'))
        productDescription.grid(column=1, row=7, padx=10, pady=10, sticky="w")


        self.submit_record_btn = Button(self.displayLabel, cursor = "hand2", text = "Record", command = self.createRecord,
                                        font=('Times New Roman', int(FR*20)), bg='#648EF1', fg='#FFFFFF', border=0)
        self.submit_record_btn.grid(column = 0, row = 8, padx = 10, pady = 20, sticky = "se")
        
        tips = Label(self.displayLabel, text = "*record validations:-",font =('Times New Roman',int(FR*10),'underline'), fg = 'red', bg ='white')
        tips.grid(column=0,row=9, padx=5, pady=10, sticky="w")

        tips = Label(self.displayLabel, text="- check for the product in inventory before recording",
                     font=('Times New Roman', int(FR*10)), fg='red', bg='white')
        tips.grid(column=0, row=10, padx=5, pady=0, sticky="w",columnspan = 2)

        tips = Label(self.displayLabel, text="- recording of similar product will pop error msg",
                     font=('Times New Roman', int(FR*10)), fg='red', bg='white')
        tips.grid(column=0, row=11, padx=5, pady=0, sticky="w", columnspan=2)

        tips = Label(self.displayLabel, text="- ensure all fields are filled before recording",
                     font=('Times New Roman', int(FR*10)), fg='red', bg='white')
        tips.grid(column=0, row=12, padx=5, pady=0, sticky="w", columnspan = 2)

        tips = Label(self.displayLabel, text="- 'Quantity' and 'Sales Price' must be a number",
                     font=('Times New Roman', int(FR*10)), fg='red', bg='white')
        tips.grid(column=0, row=13, padx=5, pady=0, sticky="w", columnspan=2)





    #Update The Product Details in Inventory

    def updateInventory(self):
        self.displayFrame.destroy()
        self.displayFrame = Frame(self.inventory, bg = '#FFFFFF')
        self.displayFrame.pack(fill="both", side="left")

        self.searchFrame = Frame(self.displayFrame, bg='#4F83FC')
        self.searchFrame.pack(pady = 10)  # fill ='x', side = 'left', anchor = N

        def getObjectIid():
            row_iid = viewTree.focus()
            if(row_iid == ''):
                return 0
            else:
                return row_iid

        def displayUpdatePopup(displayText,cmd):
            self.UpdatePopUp = Toplevel()
            self.UpdatePopUp.grab_set()
            self.UpdatePopUp.iconbitmap('./res/dsk.ico')
            self.UpdatePopUp.title("Update Values")
            
            self.UpdatePopUp.geometry("+%d+%d" % (400, 300))
            self.UpdatePopUp.minsize(250,200)

            self.updateLabel = Label(self.UpdatePopUp, text=displayText)
            self.updateLabel.pack(padx=10, pady=10)
            self.updateEntry = Entry(self.UpdatePopUp, width=20)
            self.updateEntry.pack(padx=10, pady=10)
            self.updateEntry.focus()
            self.updateEntry.bind('<Return>', cmd)
            updateBtn = Button(self.UpdatePopUp, text="Update Value", command=cmd)
            updateBtn.pack(padx=10, pady=20)




        def dbsQuantityUpdate(event=''):
            try:
                iid = self.row_iid
                grabbedValue = int(self.updateEntry.get())
                if (grabbedValue == 0):
                    raise ValueError
                
                # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                # db = client.get_database('saiRecords')
                # collection = db.inventory
                
                ##For local Storage
                connection = pymongo.MongoClient("localhost", 27017)
                database = connection['saiRecords']
                collection = database['inventory']

                databaseRow = collection.find_one({'_id': ObjectId(iid)}, {'Quantity': 1, '_id': 0})
                # connection.close()
                currentValue = databaseRow['Quantity']
                currentValue = int(currentValue)
                newValue = grabbedValue + currentValue
                collection.update_one({'_id': ObjectId(iid)}, {'$set': {'Quantity': newValue}})
                self.UpdatePopUp.destroy()
                self.warnUser("Value Updated")
                displaySearchResult()
            except ValueError:
                messagebox.showerror('Error', 'Value Missing or Insufficient')
                self.UpdatePopUp.destroy()

        def dbsCostUpdate(event = ''):
            try:
                iid = self.row_iid
                grabbedValue = int(self.updateEntry.get())
                if (grabbedValue == 0):
                    raise ValueError

                # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                # db = client.get_database('saiRecords')
                # collection = db.inventory

                ##For local Storage
                connection = pymongo.MongoClient("localhost", 27017)
                database = connection['saiRecords']
                collection = database['inventory']

                collection.update_one({'_id': ObjectId(iid)}, {'$set': {'Sales Price': grabbedValue}})
                self.UpdatePopUp.destroy()
                self.warnUser("Value Updated")
                displaySearchResult()
            except ValueError:
                messagebox.showerror('Error', 'Value Missing or Insufficient')
                self.UpdatePopUp.destroy()

        def dbsLocationUpdate(event = ''):
            try:
                iid = self.row_iid
                grabbedValue = self.updateEntry.get()
                if (grabbedValue == 0):
                    raise ValueError
                grabbedValue = str(grabbedValue)

                # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                # db = client.get_database('saiRecords')
                # collection = db.inventory

                ##For local Storage
                connection = pymongo.MongoClient("localhost", 27017)
                database = connection['saiRecords']
                collection = database['inventory']

                collection.update_one({'_id': ObjectId(iid)}, {
                                    '$set': {'Location': grabbedValue}})
                self.UpdatePopUp.destroy()
                self.warnUser("Value Updated")
                displaySearchResult()
            except ValueError:
                messagebox.showerror('Error', 'Value Missing or Insufficient')
                self.UpdatePopUp.destroy()

        def updateQuantityDbs():
            self.row_iid = getObjectIid()
            if self.row_iid == 0:
                self.warnUser("One Record Selection Required !")
            else:
                displayUpdatePopup("Add Quantity", dbsQuantityUpdate)

        def updateCostDbs():
            self.row_iid = getObjectIid()
            if self.row_iid == 0:
                self.warnUser("One Record Selection Required !")
            else:displayUpdatePopup("Update Value", dbsCostUpdate)


        def updateLocationDbs():
            self.row_iid = getObjectIid()
            if self.row_iid == 0:
                self.warnUser("One Record Selection Required !")
            else:displayUpdatePopup("Update Value", dbsLocationUpdate)




        def displaySearchResult(event = ""):
            searchResult = []
            # print("Checking Search Result")
            # print(searchResult)
            clearTree()
            searchValue = self.searchEntry.get()
            # print(searchValue)

            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database('saiRecords')
            # collection = db.inventory

            ##For Local Database
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
                self.warnUser("Product Not Found")
                print("Warned !!!!!!!")
            else:
                showCondition = True
            if (showCondition == TRUE):
                print("Printing Results")
                self.txt = 0
                for x in searchResult:
                    print("Inside Second Loop")
                    viewTree.insert(parent='', index=END, iid=(x["_id"]), text=(self.txt+1), values=(
                        x['Product Name'], x['Cost Price'], x['Sales Price'], x['Quantity'], x['Units'], x['Location'], x['Purchased From']))
                    self.txt += 1
                    print("End of loop ")
                    print("Exited For Loop")
            print("Exited If ELse Statement")
        # searchLabel = Label(self.searchFrame, text="Product", bg='#4F83FC', fg = '#FFFFFF')
        # searchLabel.grid(column=0, row=1, padx=10, pady=10, sticky="w")

        def clearPlaceHolder(event):
            self.searchEntry.delete(0,'end')
        
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
                    ##For Local Database
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

        self.searchEntry = Entry(self.searchFrame, width = int(WR*40), bg='#4F83FC', fg='#FFFFFF',border=0, font=('Comic Sans MS', int(FR*15)))
        self.searchEntry.grid(column=1, row=1, padx=10, pady=10, sticky="w")
        self.searchEntry.insert(0,'search for...')
        self.searchEntry.bind('<FocusIn>', clearPlaceHolder)
        self.searchEntry.bind('<KeyRelease>', displaySearchResult)
        self.searchEntry.bind('<Return>',displaySearchResult)

        searchBtn=Button(self.searchFrame, text = "GO", command = displaySearchResult,
        font=('Times New Roman', int(FR*18),'bold','underline'), bg='#4F83FC', fg = '#FFFFFF',border = 0, cursor = "hand2")
        searchBtn.grid(column=2, row=1, padx=10, pady=10, sticky="w")
        

        self.rsltFrame = Frame(self.displayFrame, bg = 'white')
        self.rsltFrame.pack() #fill = 'both', side = 'left', anchor = S

        lb = Label(self.rsltFrame, text = 'Search Result', font = ('Helvetica',int(FR*15),'bold','underline'), bg = 'white')
        lb.pack(pady = 20)
        #Table view starts from here
        viewTree = ttk.Treeview(self.rsltFrame,height = int(HR*8), style="mystyle.Treeview")

        #Define Columns
        viewTree['columns'] = ('Product Name', 'Cost Price' ,'Sales Price', 'Quantity','Units' , 'Location')
        viewTree.column('#0', width = int(WR*60), minwidth=10, anchor=CENTER)
        viewTree.column('Product Name', width = int(WR*350), anchor=W)
        viewTree.column('Cost Price', width = int(WR*138), anchor=CENTER)
        viewTree.column('Sales Price', width = int(WR*138), anchor=CENTER)
        viewTree.column('Quantity', width = int(WR*130), anchor=CENTER)
        viewTree.column('Units', width = int(WR*110), anchor=CENTER)
        viewTree.column('Location', width = int(WR*150), anchor=CENTER)
        
        #Create Headings
        viewTree.heading('#0', text='S.N', anchor=CENTER)
        viewTree.heading('Product Name', text='Product Name', anchor=W)
        viewTree.heading('Cost Price', text='Cost Price', anchor=CENTER)
        viewTree.heading('Sales Price', text='Sales Price', anchor=CENTER)
        viewTree.heading('Quantity', text='Quantity', anchor=CENTER)
        viewTree.heading('Units', text='Units', anchor=CENTER)
        viewTree.heading('Location', text='Location', anchor=CENTER)
        
        viewTree.pack(padx = 10)

        def clearTree():
            for rows in viewTree.get_children():
                viewTree.delete(rows)

        self.btnFrame = Frame(self.displayFrame, bg='pink')
        self.btnFrame.pack()

        addQuantity = Button(
            self.btnFrame, text='Add Quantity', command= updateQuantityDbs)
        addQuantity.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        changeCost = Button(self.btnFrame, text = "Update Cost", command = updateCostDbs)
        changeCost.grid(column=1, row=0, padx=10, pady=10, sticky="w")

        changeLocation = Button(
            self.btnFrame, text="Update Location", command=updateLocationDbs)
        changeLocation.grid(column=2, row=0, padx=10, pady=10, sticky="w")

        phaseoutBtn = Button(self.btnFrame, text='Phase Out Product', command=phaseOutProducts)
        phaseoutBtn.grid(column=3, row=0, padx=10, pady=10, sticky="w")

    def viewOrders(self):
        self.displayFrame.destroy()
        self.displayFrame = Frame(self.inventory)
        self.displayFrame.pack(fill="both")

        topFrame = Frame(self.displayFrame)
        topFrame.pack()

        orderDetailsFrame = Frame(self.displayFrame)
        orderDetailsFrame.pack()
        def validateContact(e):
            try:
                value=int(customerPhoneEntry.get())
            except ValueError:
                customerPhoneEntry.delete(-1,'end') 

        def displayOrderSearch(event=''):
            example = []
            self.view_productId = []
            searchValue = searchBox.get()
            key = PtypeCombo.get()
            try:
                if (key == ""):
                    raise ValueError
                else:
                    #For Local database Storage
                    connection = pymongo.MongoClient("localhost", 27017)
                    database = connection['saiRecords']
                    collection = database['order']
                    if (key == 'By Customer'):
<<<<<<< HEAD
                        viewTree.heading('Customer Name', text='Product Name', anchor=CENTER)
                        customerNameOrProductName.config(text="Product Name: ")
=======
                        customerNameLabel.grid(column =1,row =0)
                        customerNameEntry.grid(column=2,row=0)
                        customerPhoneLabel.grid(column =1,row =1)
                        customerPhoneEntry.grid(column=2,row=1)
                        customerPhoneEntry.bind('<KeyRelease>',validateContact)
                        searchBox.grid_forget()
                        viewTree.heading('Customer Name', text='Product Name', anchor=CENTER)
                        customerNameOrProductName.config(text="Customer Name: ")
>>>>>>> 2447d4b5d4e611af496bf09a2df3d8662bbb1617
                        searchFilter = 'i'
                        result = collection.find({'Customer Name': {'$regex': searchValue, '$options': searchFilter}})  
                        for x in result:
                            example.append(x['Customer Name'] + ' -- ' + x['Date'] + ' -- ' +  x['Contact Number'])
                            self.view_productId.append(x['_id'])
                        
                    else:
<<<<<<< HEAD
                        viewTree.heading('Customer Name', text='Customer Name', anchor=CENTER)
                        customerNameOrProductName.config(text="Customer Name: ")
                        requiredId = []
                        result= collection.find({})
                        
                    #     for i in result:
                    #         s1 = i["Products"]
                    #         for j in s1:                                
                    #             final.append({
                    #                             "Product Name":j,
                    #                             "Custumer Name": i["Customer Name"],
                    #                             "Quantity": s1[j]['Quantity'],
                    #                             "Sales Price":s1[j]['Sales Price'],
                    #                             "Units": s1[j]["Units"],
                    #                             "Product Total": s1[j]["Product Total"]       
                    #                         })
                    #             if searchValue.upper() in str(j.upper()):
                    #                 example.append(j + ' -- ' + str(s1[j]['Quantity']))  
                    itemlistbox.insert(0, *example)
=======
                        customerNameEntry.grid_forget()
                        customerNameLabel.grid_forget()
                        customerPhoneEntry.grid_forget()
                        customerPhoneLabel.grid_forget()
                        searchBox.grid(column=1, row=0, padx = 10, pady=10,columnspan=3)
                        searchBox.bind('<KeyRelease>', displayOrderSearch)
                        searchBox.bind('<Return>')
                        viewTree.heading('Customer Name', text='Customer Name', anchor=CENTER)
                        customerNameOrProductName.config(text="Product Name: ")
                        final = []
                        result= collection.find({})
                        for i in result:
                            s1 = i["Products"]
                            for j in s1:                                
                                final.append({
                                                "Product Name":j,
                                                "Custumer Name": i["Customer Name"],
                                                "Quantity": s1[j]['Quantity'],
                                                "Sales Price":s1[j]['Sales Price'],
                                                "Units": s1[j]["Units"],
                                                "Product Total": s1[j]["Product Total"]       
                                            })
                                if searchValue.upper() in str(j.upper()):
                                    example.append(j + ' -- ' + str(s1[j]['Quantity']))  
>>>>>>> 2447d4b5d4e611af496bf09a2df3d8662bbb1617

                    # if (len(self.view_productId) < 1):
                    #     messagebox.showinfo("Search Request", "No Record Found")
                    
            except ValueError:
                messagebox.showerror("Invalid Request", "Set Search Filter")
           
        
        PtypeCombo = ttk.Combobox(topFrame, background='#CED7D7',width = int(WR*10), values=['By Customer', 'By Product'],font=('Comic Sans MS',int(FR*10),'bold'),state = 'readonly')
        PtypeCombo.current(0)
        PtypeCombo.grid(column = 0, row = 0, padx = 5, pady = 10, sticky = "w")
        PtypeCombo.bind('<<ComboboxSelected>>', displayOrderSearch)


        searchBox = Entry(topFrame, font=('Hevitica', int(FR*13),'bold'), width=int(WR*20))
        searchBox.grid_forget()

        customerNameLabel = Label(topFrame,text="Name: ", font=('Comic Sans MS', int(FR*12)))
        customerNameLabel.grid(column =1,row =0)
        
        customerNameEntry = Entry(topFrame, font=('Hevitica', int(FR*11),'bold'), width= int(WR*15))
        customerNameEntry.grid(column=2,row=0)

        customerPhoneLabel = Label(topFrame,text="Mobile Number: ", font=('Comic Sans MS', int(FR*12)))
        customerPhoneLabel.grid(column =1,row =1)

        customerPhoneEntry = Entry(topFrame, font=('Hevitica', int(FR*11),'bold'), width= int(WR*15))
        customerPhoneEntry.grid(column=2,row=1)
        customerPhoneEntry.bind('<KeyRelease>',validateContact)

        btn_search = Button(topFrame, text='Search', bg = '#3399ff', fg = '#ffffff', border = 0,font=('Comic Sans MS', int(FR*13),'bold'),command=displayOrderSearch)
        btn_search.grid(row=0, column=4, padx = 11, pady = 10,rowspan=2)

        # itemlistbox = Listbox(topFrame, width = int(WR*40), height = int(HR*4), bg="#e8eddf", font =('Comic Snas MS', int(FR*15) ))
        # itemlistbox.grid(row=1,column = 0,columnspan=3,padx=5)

        # scrollbar = Scrollbar(topFrame, orient=VERTICAL)
        # scrollbar.config(command=self.itemlistbox.yview)
        # scrollbar.grid(row=1,ipadx=10,column=3,sticky='ns')
        
        customerNameOrProductName = Label(orderDetailsFrame,text='Customer Name: ',font=('Comic Sans MS', int(FR*13)))
        customerNameOrProductName.pack()
        customerNameOrProductName.pack_forget()
        
        viewTree = ttk.Treeview(orderDetailsFrame,  style="mystyle.Treeview", height=10)

        #Define Columns
        viewTree['columns'] = ('Customer Name',
                               'Sales Price', 'Quantity', 'Units', 'Total Price')
        viewTree.column('#0', width = int(WR*40), minwidth=10, anchor=CENTER)
        viewTree.column('Customer Name', width = int(WR*130), anchor=CENTER)
        viewTree.column('Sales Price', width = int(WR*120), anchor=CENTER)
        viewTree.column('Quantity', width = int(WR*100), anchor=CENTER)
        viewTree.column('Units', width = int(WR*90), anchor=CENTER)
        viewTree.column('Total Price', width = int(WR*130), anchor=CENTER)

        #Create Headings
        viewTree.heading('#0', text='S.N', anchor=CENTER)
        viewTree.heading('Customer Name', text='Customer Name', anchor=CENTER)
        viewTree.heading('Sales Price', text='Sales Price', anchor=CENTER)
        viewTree.heading('Quantity', text='Quantity', anchor=CENTER)
        viewTree.heading('Units', text='Units', anchor=CENTER)
        viewTree.heading('Total Price', text='Total Price', anchor=CENTER)
        viewTree.pack(fill = 'both',expand = 1, padx = 20,pady = 20)
        self.viewTree = viewTree
        
        
    # Displays the items in the inventory
    def viewInventory(self):
        self.displayFrame.destroy()
        self.displayFrame = Frame(self.inventory)
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
            # print("Checking Search Result")
            # print(searchResult)
            clearTree()
            searchValue = self.searchEntry.get()
            # print(searchValue)

            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database('saiRecords')
            # collection = db.inventory
            ##For local Database Storage
            connection = pymongo.MongoClient("localhost", 27017)
            database = connection['saiRecords']
            collection = database['inventory']
            searchResult = collection.find(
                {"Product Name": {'$regex': searchValue, '$options': 'i'}})
            searchResult2 = collection.find(
                {"Product Name": {'$regex': searchValue, '$options': 'i'}})

            connection.close()
            showCondition = FALSE
            lenCheck = len(list(searchResult2))

            if (lenCheck == 0):
                self.warnUser("Product Not Found")
                print("Warned !!!!!!!")
            else:
                showCondition = True
            if (showCondition == TRUE):
                print("Printing Results")
                self.txt = 0
                for x in searchResult:
                    print("Inside Second Loop")
                    viewTree.insert(parent='', index=END, iid=(x["_id"]), text=(self.txt+1), values=(
                        x['Product Name'], x['Cost Price'], x['Sales Price'], x['Quantity'], x['Units'], x['Location'], x['Purchased From']))
                    self.txt += 1
                    print("End of loop ")
                    print("Exited For Loop")
            print("Exited If ELse Statement")

        self.searchEntry = Entry(searchFrame, width = int(WR*40), bg='#4F83FC', fg='#FFFFFF',border=0, font=('Comic Sans MS', int(FR*20)))
        self.searchEntry.grid(column=1, row=1, padx=10, pady=10, sticky="w")
        self.searchEntry.insert(0,'search for...')
        self.searchEntry.bind('<FocusIn>', clearPlaceHolder)
        self.searchEntry.bind('<KeyRelease>', displaySearchResult)
        self.searchEntry.bind('<Return>',displaySearchResult)

        searchBtn=Button(searchFrame, text = "GO", command = displaySearchResult,
        font=('Times New Roman', int(FR*18),'bold','underline'), bg='#4F83FC', fg = '#FFFFFF',border = 0, cursor = "hand2")
        searchBtn.grid(column=2, row=1, padx=10, pady=10, sticky="w")

        
        viewTree = ttk.Treeview(self.displayFrame,  style="mystyle.Treeview", height=5)

        #Define Columns
        viewTree['columns'] = ('Product Name', 'Cost Price',
                               'Sales Price', 'Quantity', 'Units', 'Location','Purchased From')
        viewTree.column('#0', width = int(WR*60), minwidth=10, anchor=CENTER)
        viewTree.column('Product Name', width = int(WR*200), anchor=W)
        viewTree.column('Cost Price', width = int(WR*138), anchor=CENTER)
        viewTree.column('Sales Price', width = int(WR*138), anchor=CENTER)
        viewTree.column('Quantity', width = int(WR*130), anchor=CENTER)
        viewTree.column('Units', width = int(WR*110), anchor=CENTER)
        viewTree.column('Location', width = int(WR*150), anchor=CENTER)
        viewTree.column('Purchased From', width = int(WR*150), anchor=CENTER)

        #Create Headings
        viewTree.heading('#0', text='S.N', anchor=CENTER)
        viewTree.heading('Product Name', text='Product Name', anchor=W)
        viewTree.heading('Cost Price', text='Cost Price', anchor=CENTER)
        viewTree.heading('Sales Price', text='Sales Price', anchor=CENTER)
        viewTree.heading('Quantity', text='Quantity', anchor=CENTER)
        viewTree.heading('Units', text='Units', anchor=CENTER)
        viewTree.heading('Location', text='Location', anchor=CENTER)
        viewTree.heading('Purchased From', text='Purchased', anchor=CENTER)
        viewTree.pack(fill = 'both',expand = 1, padx = 20,pady = 20)
        self.viewTree = viewTree

        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.inventory
        ##For local database Storage
        connection = pymongo.MongoClient("localhost", 27017)
        database = connection['saiRecords']
        collection = database['inventory']

        inventorydata= collection.find()

        self.txt=0
        for x in inventorydata:
            qnty = x['Quantity']
            if (qnty== 0):
                qnty = "Out of Stock"
            viewTree.insert(parent='', index=END , iid=(x["_id"]), text =(self.txt+1), values =(x['Product Name'],x['Cost Price'], x['Sales Price'], qnty,x['Units'],x['Location'],x['Purchased From']))
            self.txt+=1
        self.btnFrame = Frame(self.displayFrame, bg='pink')
        self.btnFrame.pack()
        connection.close()

        

    #Creates self.displayFrame for selection of Salary or Wages Record




    # creates frame and buttons inside the Billing tab's Navigation Button
    def navigationFrame_billing(self,tab):
    
        if 1:
            self.billing_method = 0

        def order():
            if self.billing_method == 0:
                viewProductsInBill()
                if (self.billingTotalAmount != 0):
                    validate = messagebox.askokcancel("Billing on Process","Do you want to swiitch to Order ? ")
                    if (validate):
                        self.productsInBill = {}
                        self.billingTotalAmount = 0
                        self.billingAmountLabel.config(text=self.billingTotalAmount)
                        viewProductsInBill()
                        self.billing_method = 1
                        #templabel.grid(row= 1,column=6)
                        self.billtypelabel.config(text='Order')
                        self.billingVatableAmountLabel.grid_forget()
                        self.VatableAmountLabel.grid_forget()
                else:
                    self.billing_method = 1
                    self.billtypelabel.config(text='Order')
                    #templabel.grid(row= 1,column=6)
                    self.billingVatableAmountLabel.grid_forget()
                    self.VatableAmountLabel.grid_forget()
                    

                    
        
        def vat_billing():
            if self.billing_method ==1:
                viewProductsInBill()
                if (self.billingTotalAmount != 0):
                    validate = messagebox.askokcancel("Billing on Process","Do you want to swiitch to VAT Billing ? ")
                    if (validate):
                        self.productsInBill = {}
                        self.billingTotalAmount = 0
                        self.billingAmountLabel.config(text=self.billingTotalAmount)
                        viewProductsInBill()
                        self.billing_method = 0
                        self.billtypelabel.config(text='VAT BILLING')
                        self.billingVatableAmountLabel.grid(row=1, column=1, sticky="n",  pady=0)
                        self.VatableAmountLabel.grid(row=1, column=0, sticky="n",  pady=0)
                        self.billingVatableAmountLabel.config(text = 0)

                        #templabel.grid_forget()                     
                else:
                    self.billing_method = 0
                    self.billtypelabel.config(text='VAT BILLING')
                    self.billingVatableAmountLabel.grid(row=1, column=1, sticky="n",  pady=0)
                    self.VatableAmountLabel.grid(row=1, column=0, sticky="n",  pady=0)
                    self.billingVatableAmountLabel.config(text = 0)
                    
                
                    #templabel.grid_forget()
                



        buttonBg = "#284F9B"

        self.buttonFrame = Frame(tab, bg=buttonBg)
        self.buttonFrame.pack(side = LEFT,fill= Y)

        s_btn = ttk.Style()
        s_btn.configure('TButton', height = int(HR*3), width = int(WR*20),border=0,
        background=buttonBg,
        font=("Helvetica",int(FR*14),'bold'))
        s_btn.map('TButton',
              foreground=[('disabled', 'yellow'),
                          ('pressed', 'red'),
                          ('active', '#5A63F5')],
              background=[('disabled', 'magenta'),
                          ('pressed', '!focus', 'cyan'),
                          ('active', 'green')],
              
              )

        self.btn_addProduct = ttk.Button(self.buttonFrame, text = "VAT Billing",style ='TButton', command = vat_billing)
        self.btn_addProduct.grid(column = 0 , row = 1, pady = 10)

        self.btn_update = ttk.Button(self.buttonFrame, text="Order", style='TButton', command=order)
        self.btn_update.grid(column=0, row=2, pady=5)


        self.displayFrame = Frame(tab,bg ="white")
        self.displayFrame.pack(fill = 'both')

        self.billingtypeFrame = Frame(self.displayFrame,bg='white')
        self.billingtypeFrame.pack(fill='x')
        
        self.mainBillingFrame =Frame(self.displayFrame,bg='white')
        self.mainBillingFrame.pack(side='left', fill='both', padx=20, pady=25, ipady=10)

        self.billingButtonFrame = Frame(self.displayFrame, bg = 'white')
        self.billingButtonFrame.pack(side = 'left', fill = 'both', pady = 15,ipady=10)
        # self.billingButtonFrame.grid(column=1, row=0, sticky=NS)

        

        self.billingSearchFrame=Frame(self.mainBillingFrame,bg='white')
        self.billingSearchFrame.pack(padx= 30)
        # self.billingSearchFrame.grid(column = 0, row = 0, pady = 15)

        self.billingFrame = Frame(self.mainBillingFrame, bg='white')
        self.billingFrame.pack( padx= 10, pady = 10)
        # self.billingFrame.grid(column = 0, row = 1, pady = 15)

        self.amountFrame = Frame(self.mainBillingFrame, bg='white')
        self.amountFrame.pack(pady = 10)
        # self.amountFrame.grid(column = 0, row = 2)


        
        
        #Clears the billing 
        def clearBilling():
            try:
                if (self.productsInBill == {}):
                    raise ValueError
                validate = messagebox.askokcancel("Billing on Process","Do you want to Clear Billing ? ")
                if (validate):
                    self.productsInBill = {}
                    self.billingTotalAmount = 0
                    self.billingAmountLabel.config(text=self.billingTotalAmount)
                    self.billingVatableAmountLabel.config(text = 0)
                    
                    
                    viewProductsInBill()
            except ValueError:
                messagebox.showinfo("Invalid Request", "Billing process not initited yet.")

        # Saves Bill to database
        def completeBilling():
            #Assigns customer's name to the bill and saves to dbs
            def saveBilltoDbs(event =''):
                try:
                    if ((askEntry.get()) == ""):
                        raise ValueError

                    
                    # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                    # db = client.get_database('saiRecords')
                    # collection = db.inventory

                    ##For Local Storage
                    connection = pymongo.MongoClient("localhost", 27017)
                    database = connection['saiRecords']
                    collection = database['inventory']
                    for product in self.productsInBill:
                        print(product)
                        orgValue = int((collection.find_one({'Product Name': product}))['Quantity'])
                        orgValue_sold = int((collection.find_one({'Product Name': product}))['Sold'])
                        orgValue_order = int((collection.find_one({'Product Name': product}))['Order'])
                        newValue = orgValue-int(self.productsInBill[product]['Quantity'])
                        print(newValue)
                        collection.find_one_and_update({'Product Name': product},
                        {'$set':{
                            'Quantity': (orgValue-int(self.productsInBill[product]['Quantity'])),
                        }})
                        if self.billing_method == 0:
                            collection = database['inventory']
                            collection.find_one_and_update({'Product Name': product},
                            {'$set':{
                                'Sold': (orgValue_sold+int(self.productsInBill[product]['Quantity'])),
                            }})
                        else:
                            collection = database['inventory']
                            collection.find_one_and_update({'Product Name': product},
                            {'$set':{
                                'Order': (orgValue_order+int(self.productsInBill[product]['Quantity'])),
                            }})
                    dateTime = self.getDateTime()
                    billDict = {}
                    billDict['Date'] = dateTime[0]
                    billDict['Time'] = dateTime[1]
                    billDict['Customer Name'] = askEntry.get()
                    billDict['Contact Number'] = phnNumEntry.get()
                    #Processing the products in bill '.' -> '?'
                    new_dict = {}
                    a= self.productsInBill
                    print(type(new_dict))
                    for items in a:
                        if '.' in items:
                            processed_string = items.replace('.', '?')
                            new_dict[processed_string] = a[items]
                        else:
                            new_dict[items] = a[items]
                    print(self.productsInBill)
                    billDict['Products']={}
                    billDict['Products']=new_dict
                    if self.billing_method == 0:
                        billDict['Vatable'] = int(self.billingTotalAmount)
                        billDict['Grand Total'] = int(int(self.billingTotalAmount)+0.13*int(self.billingTotalAmount))
                        collection = database['sales']
                        print("bill saved to vat bill")
                    else:
                        billDict['Grand Total'] = int(self.billingTotalAmount)
                        collection = database['order']
                        print("bill saved to order data set")
                    # collection = db.sales

                    collection.insert_one(billDict)
                    #Logic to Add value to daily Sales
                    # collection = db.dailySalesData
                    collection = database['dailySalesData']
                    dte = dateTime[0]
                    newValue = self.billingTotalAmount
                    if (collection.count_documents({'_id': dte}) > 0):
                        collection.find_one_and_update(
                            {'_id': dte}, {'$inc': {'daySales': newValue}})
                    else:
                        collection.insert_one({'_id': dte, 'daySales': self.billingTotalAmount})
                    top.destroy()
                    self.productsInBill = {}
                    self.billingTotalAmount = 0
                    self.billingAmountLabel.config(text=self.billingTotalAmount)
                    # connection.close()
                    viewProductsInBill()
                    messagebox.showinfo('Transaction Completed','Bill saved to Database')
                except ValueError:
                    messagebox.showerror("Insuccifient Data", "Provide Customer Name")



            if (len(self.productsInBill)<1):
                messagebox.showerror("error", "No Products in Bill ! ")
            else:
                proceedBilling = messagebox.askokcancel("Conformation Required", "Conform Billing ?")
                if(proceedBilling == 1):

                    def validateContact(e):
                        try:
                            value=int(phnNumEntry.get())
                        except ValueError:
                            phnNumEntry.delete(-1,'end')   

                    top = Toplevel()
                    top.grab_set()
                    top.iconbitmap('./res/dsk.ico')
                    top.title("Enter Name")
                    top.geometry("+%d+%d" % ( 500, 500))
                    askLable = Label(top, text = 'Customer Name : ', font = ('Helvetica', int(FR*15), 'bold') )
                    askLable.grid(row = 0, column = 0, padx = 5, pady = 5)
                    
                    askEntry = Entry(top, width = int(WR*30), font=('Comic Sans MS', int(FR*15), 'bold'))
                    askEntry.grid(row = 0, column = 1, padx = 5, pady = 5)
                    askEntry.bind('<Return>',saveBilltoDbs)
                    askEntry.focus_set()
                    phnNum = Label(top, text = 'Contact Number : ', font = ('Helvetica', int(FR*15), 'bold') )
                    phnNum.grid(row = 1, column = 0, padx = 5, pady = 5)
                    phnNumEntry = Entry(top, width = int(WR*30), font=('Comic Sans MS', int(FR*15), 'bold'))
                    phnNumEntry.grid(row = 1, column = 1, padx = 5, pady = 5)
                    phnNumEntry.bind('<KeyRelease>',validateContact)
                    btn = Button(top, text ="Enter", width = int(WR*10), command = saveBilltoDbs)
                    btn.grid(row = 2, column = 1, padx = 5, pady = 5)
                    





        #Displays Product in the Listbox of billing tabs to search for Product
        def displayProductOptions(event = ''):
            example = []
            searchValue = self.billingSearchEntry.get()

            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database('saiRecords')
            # collection = db.inventory

            ##For local storage
            connection = pymongo.MongoClient("localhost", 27017)
            database = connection['saiRecords']
            collection = database['inventory']
            result = collection.find(
                {"Product Name": {'$regex': searchValue, '$options' : 'i' }})
            # connection.close()
            for x in result:
                example.append(x['Product Name'])
            self.itemlistbox.delete(0,END)
            self.itemlistbox.insert(0, *example)

        def viewProductsInBill():
            count = 0
            self.billingTotalAmount=0
            for rows in viewTree.get_children():
                viewTree.delete(rows)

            for values in self.productsInBill:
                viewTree.insert(parent='', index=END, iid=(self.productsInBill[values]['iid']),
                                text=(count+1),
                                values=(values,
                            self.productsInBill[values]['Quantity'],
                            self.productsInBill[values]['Units'],
                            self.productsInBill[values]['Sales Price'],
                            self.productsInBill[values]['Product Total']
                            
                            ))
                self.billingTotalAmount += int(self.productsInBill[values]['Product Total'])
                self.billingAmountLabel.config(text=self.billingTotalAmount)

                self.billingAmountLabel.focus()
                
                if self.billing_method ==0:
                    self.billingVatableAmountLabel.config(text = int(self.billingTotalAmount))
                    self.billingAmountLabel.config(text = int(self.billingTotalAmount+0.13*self.billingTotalAmount))
                
                count += 1
            print('Products in Bill')
            print(self.productsInBill)

       #New Add Product Funtion to add products in bill
        def billingProcess():
            try:                  
                def displayToBillView(event=''):
                    
                    requiredQuantity = float(askQuantityEntry.get())
                    top.destroy()

                    # messagebox.showerror('Invalid Request', 'Quantity must be a number')

                    if (float(productToBill['Quantity']) < requiredQuantity or requiredQuantity < 1):
                        self.warnUser("Invalid Entry. Please Check the Available Quantity")
                        billingProcess()
                    else:
                        # try:
                        if (productToBill['Product Name'] in self.productsInBill.keys()):
                            self.warnUser("Product Already in Bill")
                            top.destroy()
                        else:
                            productTotal = int(productToBill['Sales Price'])*requiredQuantity
                            self.productsInBill[productToBill['Product Name']] = {}
                            self.productsInBill[productToBill['Product Name']]['Quantity'] = requiredQuantity
                            self.productsInBill[productToBill['Product Name']]['iid'] = productToBill['_id']
                            self.productsInBill[productToBill['Product Name']]['Sales Price'] = productToBill['Sales Price']
                            self.productsInBill[productToBill['Product Name']]['Units'] = productToBill['Units']
                            self.productsInBill[productToBill['Product Name']]['Product Total'] = productTotal
                            viewProductsInBill()
                            top.destroy()

                            

                # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                # db = client.get_database('saiRecords')
                # collection = db.inventory
                
                ##For local database storage
                
                connection = pymongo.MongoClient("localhost", 27017)
                database = connection['saiRecords']
                collection = database['inventory']
                toadd = self.itemlistbox.get(ANCHOR)
                print("Selected from itemlistbox" + toadd)

                productToBill = collection.find_one({'Product Name': toadd})
                
                if (productToBill['Quantity']==0):
                    raise ValueError

                # connection.close()                    
                top = Toplevel()
                top.grab_set()
                top.iconbitmap('./res/dsk.ico')
                top.geometry("+%d+%d" % (400, 400))

                availableQuantity = Label(
                    top, text="Available Quantity", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
                availableQuantity.grid(row=0, column=0)
                displayAvailableQuantity = Label(top, text=(str(productToBill['Quantity'])+" "+ str(productToBill['Units'])), padx=5, pady=5, font=('Comic Sans MS', int(FR*15), 'bold'))
                displayAvailableQuantity.grid(row=0, column=1)

                salesPriceLbl = Label(top, text="Sales Price", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
                salesPriceLbl.grid(row = 1, column= 0)

                salesPriceDsp = Label(top, text=productToBill['Sales Price'], padx=5, pady=5,font=('Helvetica', 15, 'bold'))
                salesPriceDsp.grid(row = 1, column=1)

                
                askQuantityLabel = Label(top, text="Enter Quantity", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
                askQuantityLabel.grid(row=2, column=0)

                askQuantityEntry = Entry(top, width = int(WR*10), font=('Comic Sans MS', int(FR*15), 'bold'))
                askQuantityEntry.grid(row=2, column=1)
                askQuantityEntry.focus()
                askQuantityEntry.bind('<Return>', displayToBillView)

                okBtn = Button(top, text="Sell", padx=5,pady=10, width = int(WR*8),font=('Georgia', int(FR*10),'bold'), command=displayToBillView)
                okBtn.grid(row=3, column=0)

            except TypeError:
                self.warnUser("Product Selection Required")
                # top.destroy()
            except ValueError:
                messagebox.showerror('Invalid Request', 'The selected product seems Out of Stock. Try adding the product in the inventory')
        
        def billingEditProcess():
            def applyEdits(event=''):

                newValue = float(quantityEntry.get())
                try:
                    if (newValue <= 0.0 or newValue > avalQuantity):
                        raise ValueError
                    else:
                        productname = (viewTree.item(iidEdit, 'values'))[0]
                        billAmount = float((viewTree.item(iidEdit, 'values'))[4])
                        orgValue = float((viewTree.item(iidEdit, 'values'))[1])
                        unitCost = float((viewTree.item(iidEdit, 'values'))[3])
                        self.billingTotalAmount -= billAmount
                        newProductCost = unitCost*newValue
                        self.billingTotalAmount += newProductCost
                        self.productsInBill[productname]['Quantity'] = newValue
                        self.productsInBill[productname]['Product Total'] = newProductCost

                        viewTree.set(iidEdit, column='Quantity',
                                     value=newValue)
                        self.billingAmountLabel.config(text=self.billingTotalAmount)
                        viewProductsInBill()
                        top.destroy()
                except ValueError:
                    messagebox.showerror(
                        "Invalid Request", "Check For Product Availability")

            iidEdit = viewTree.focus()

            if (iidEdit == ""):
                messagebox.showwarning("Warning", "Product Selection Required")
            else:
                top = Toplevel()
                top.grab_set()
                top.geometry("+%d+%d" % (400, 400))
                top.iconbitmap('./res/dsk.ico')
                getProduct = (viewTree.item(iidEdit, 'values'))[0]
                collection = self.getConnect()
                rslt = collection.find_one({'Product Name': getProduct}, {
                                           'Quantity': 1, '_id': 0})
                avalQuantity = float(rslt['Quantity'])
                availableQuantity = Label(
                    top, text="Available Quantity", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
                availableQuantity.grid(row=0, column=0)
                displayAvailableQuantity = Label(
                    top, text=avalQuantity, padx=5, pady=5, font=('Comic Sans MS', int(FR*15), 'bold'))
                displayAvailableQuantity.grid(row=0, column=1)

                quantityLabel = Label(top, text="Enter New Quantity", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
                quantityLabel.grid(row=1, column=0)


                quantityEntry = Entry(top, width = int(WR*10),  font=('Comic Sans MS', int(FR*15), 'bold'))
                quantityEntry.grid(row=1, column=1)
                quantityEntry.focus()
                quantityEntry.bind('<Return>', applyEdits)

                editbtn = Button(top, text="Change", command=applyEdits, font=('Georgia',int(FR*10),'bold'))
                editbtn.grid(row=2, column=0, pady =12)

        #Bill Product's Quantity Edit Function
        def applyDiscountProcess():
            
            def applyDiscounts(event=''):
                
                discount_value = float(discountedValue.get())
                discount_scheme = schemeType.get()
                

                try:
                    productname = (viewTree.item(iidEdit, 'values'))[0]
                    billAmount = float((viewTree.item(iidEdit, 'values'))[4])
                    orgValue = float((viewTree.item(iidEdit, 'values'))[1])
                    unitCost = float((viewTree.item(iidEdit, 'values'))[3])
                    self.billingTotalAmount -= billAmount

                    if (discount_value == ""):
                        raise ValueError

                    if (discount_scheme == 'Product Total'):
                        self.billingTotalAmount += discount_value
                        self.productsInBill[productname]['Product Total'] = discount_value
                        viewTree.set(iidEdit, column='Total',value=discount_value)
                        new_sales_price = discount_value/orgValue
                        self.productsInBill[productname]['Sales Price'] = new_sales_price
                        viewTree.set(iidEdit, column='Sales Price',value=new_sales_price)
                        self.billingAmountLabel.config(text=self.billingTotalAmount)
                    else:
                        self.productsInBill[productname]['Sales Price'] = discount_value
                        newTotal = discount_value * float(self.productsInBill[productname]['Quantity'])
                        self.productsInBill[productname]['Product Total'] = newTotal
                        self.billingTotalAmount += newTotal
                        viewTree.set(iidEdit, column='Sales Price', value=discount_value)
                        viewTree.set(iidEdit, column='Total',value=newTotal)
                        self.billingAmountLabel.config(text=self.billingTotalAmount)
                        
                    if self.billing_method ==0:
                        self.billingVatableAmountLabel.config(text = int(self.billingTotalAmount))
                        self.billingAmountLabel.config(text = int(self.billingTotalAmount+0.13*self.billingTotalAmount))
                    top.destroy()
                    messagebox.showinfo("Transaction Complete","Discount Applied")

                    # viewTree.set(iidEdit, column='Quantity', value=newValue)
                    
                    
                except ValueError:
                    messagebox.showerror("Invalid Request", "Enter new value")
                
            
            iidEdit = viewTree.focus()
            
            if (iidEdit==""):
                messagebox.showwarning("Warning", "Product Selection Required")
            else:
                top = Toplevel()
                top.grab_set()
                top.iconbitmap('./res/dsk.ico')
                top.geometry("+%d+%d" % (300, 300))
                discountSchemeLabel = Label(top, text="Discount Scheme", font=('Helvetica', int(FR*15), 'bold'))
                discountSchemeLabel.grid(row=0, column=0, padx=5, pady=10,)

                schemeType =ttk.Combobox(top, width = int(WR*15), values=['Sales Price','Product Total'],font=('Comic Sans MS', int(FR*15), 'bold'))
                schemeType.grid(row=0, column=1, padx=5, pady=10,)
                schemeType.current(0)
                
                
                quantityLabel = Label(top, text="Enter New Value",  font=('Helvetica', int(FR*15), 'bold'))
                quantityLabel.grid(row=2, column=0,padx=5, pady=10,)

                discountedValue = Entry(top, width = int(WR*15),  font=('Comic Sans MS', int(FR*15), 'bold'))
                discountedValue.grid(row=2, column=1, padx=5, pady=10,)
                discountedValue.bind('<Return>', applyDiscounts)

                editbtn = Button(top, text="Apply Discount", command=applyDiscounts,font=('Georgia', int(FR*15), 'bold'))
                editbtn.grid(row=3, column=0, pady = 10)

        # Removes the product from the Billing Tab's Billing View Tree Table
        def removeSelectedRow():
            try:
                toDelete = viewTree.focus()
                toAddUpValues = viewTree.item(toDelete,'values')
                productName = toAddUpValues[0]
                productTotal = toAddUpValues[4]
                del self.productsInBill[productName]
                self.billingTotalAmount -= float(productTotal)
                viewProductsInBill()
                self.billingAmountLabel.config(text=self.billingTotalAmount)
                # self.productTotalLabel.config(text=self.billingTotalAmount)
                if self.billing_method ==0:
                    self.billingVatableAmountLabel.config(text = int(self.billingTotalAmount))
                    self.billingAmountLabel.config(text = int(self.billingTotalAmount+0.13*self.billingTotalAmount)) 
            except IndexError:
                self.warnUser("Product Selection Required")

        
        def callback(event = ''):
            state_left = win32api.GetKeyState(0x01)
            if state_left<0:
                billingProcess()

        #Billing GUI starts here


        #for billing name
        self.billtypelabel = Label(self.billingtypeFrame, text="VAT BILLING",
         bg='#FFFFFF', font=('Helvetica',int(FR*30),'bold','underline'),fg ="#5A63F5", border=0 )
        self.billtypelabel.pack(fill ="both",side="top")

        self.searchlabel = Label(self.billingSearchFrame, text=" Name", font=('Helvetica', int(FR*12),'bold'),bg='white')
        self.searchlabel.grid(column=0,row=1, padx = 15)
        #for search bar
        self.billingSearchEntry = Entry(self.billingSearchFrame,width = int(WR*35),font=('Helvetica', int(FR*20),'bold'), bg='#f7eeee')
        self.billingSearchEntry.grid(column = 1 , row = 1, padx = 15)
        self.billingSearchEntry.bind('<KeyRelease>',displayProductOptions)
       

        #add button button
        self.searchButton = Button(self.billingSearchFrame, text="Add Product", font = ('Helvetica', int(FR*14), 'bold'), width = int(WR*10), bg="#6aeb7b", command=billingProcess)
        self.searchButton.grid(column = 5, row = 1)

        #for listbox
        self.itemlistbox = Listbox(
            self.billingSearchFrame, width = int(WR*80), height = int(HR*5), bg="#e8eddf")
        self.itemlistbox.grid(column=1,row=2,columnspan=4,pady=0)
        self.itemlistbox.bind("<<ListboxSelect>>", callback)
        


        #for scroll bar
        self.scrollbar = Scrollbar(self.billingSearchFrame, orient=VERTICAL)
        self.scrollbar.config(command=self.itemlistbox.yview)
        self.scrollbar.grid(row=2,ipadx=10,column=5,sticky='ns')
        
       
        #treeview Styling 
        vtStyle = ttk.Style()
        vtStyle.configure('Treeview.Heading', font=('Comic Sans MS', int(FR*12), 'bold'))
        treeStyle=ttk.Style()

        treeStyle.configure("mystyle.Treeview", highlightthickness=1, bd = 0,rowheight = int(HR*25), font=('Georgia', int(FR*13)))
        # treeStyle.layout('mystyle.Treeview',[('mystyle.Treeview.treearea',{'sticky':'nswe'})])
       
       #treeview 
        viewTree = ttk.Treeview(self.billingFrame, height = int(HR*10), style="mystyle.Treeview")
        #Define Columns
        viewTree['columns']= ('Product Name','Quantity','Units', 'Sales Price','Total')
        viewTree.column('#0', width = int(WR*40), minwidth = 20, anchor = CENTER)
        viewTree.column('Product Name', width = int(WR*300), anchor = 'w')
        viewTree.column('Quantity', width = int(WR*130), anchor = CENTER)
        viewTree.column('Units', width = int(WR*60), anchor = CENTER)
        viewTree.column('Sales Price', width = int(WR*130), anchor=CENTER)
        viewTree.column('Total', width = int(WR*130), anchor=CENTER)




        #Create Headings
        viewTree.heading('#0',text='S.N', anchor = CENTER)
        viewTree.heading('Product Name', text='Product Name',anchor = CENTER)
        viewTree.heading('Quantity', text='Quantity', anchor=CENTER)
        viewTree.heading('Units', text='Units', anchor=CENTER)
        viewTree.heading('Sales Price', text='Price per unit', anchor=CENTER)
        viewTree.heading('Total', text='Total', anchor=CENTER)
        viewTree.grid(row = 0,column = 0,)
        

        #for scroll bar
        Treescrollbar = Scrollbar(self.billingFrame, orient=VERTICAL)
        Treescrollbar.config(command=viewTree.yview)
        Treescrollbar.grid(row=0,column = 1, ipadx=10, sticky='ns')

        #Edit Button
        self.editbutton = Button(
            self.billingButtonFrame, text="Edit", bg="#91cf92", command=billingEditProcess, width = int(WR*10), font=('Comic Sans MS',int(FR*12)))
        self.editbutton.grid(column=0,row=2,ipadx=8,padx=10, pady = 10)


        #Delete buttons
        self.additem = Button(self.billingButtonFrame, text="Delete",cursor ='X_cursor',font=('Comic Sans MS',int(FR*12)),bg="#f54949", width = int(WR*10), command=removeSelectedRow)
        self.additem.grid(column=0, row=3, sticky="n",padx=10, pady=10, ipadx=8)


        #Save Bill and complete Transaction
        saveBillButton = Button(self.billingButtonFrame, text="Save Bill",
                                     width = int(WR*10),  height = int(HR*2), command=completeBilling,
                                     font=('Times New Roman', int(FR*15)), bg='#648EF1', fg='#FFFFFF', border=0, cursor = 'hand2')
        saveBillButton.grid(column=0, row=4, sticky="n", padx=10, pady=10, ipadx=8)

        #amountLabel = font.Font(family = 'Helvetica', size = int(FR*22), weight = 'bold')
        #amountTotal = font.Font(family='Helvetica', size=int(FR*22), weight='bold') 

        clear_Billing = Button(self.billingButtonFrame, text="Clear Billing", bg="#f54949",cursor ='X_cursor',
                              width = int(WR*10),  font=('Helvetica', int(FR*12), 'bold'), command=clearBilling)
        clear_Billing.grid(column=0, row=5, sticky="n",padx=10, pady=20, ipadx=8)

        applyDiscountToProduct = Button(self.billingButtonFrame, text="Apply Discounts", bg='#648EF1', fg='#FFFFFF', cursor='hand2',
                                        width = int(WR*10),  font=('Helvetica', int(FR*12), 'bold'), command =applyDiscountProcess)
        applyDiscountToProduct.grid(column=0, row=6, sticky="n", padx=10, pady=20, ipadx=8)

        #for vatable amount
        self.VatableAmountLabel = Label(
            self.amountFrame, width = int(WR*10), text='Vatable        :', bg='#4A2727',font=('Helvetica',int(FR*22),'bold'), fg='#FAF712')
        self.VatableAmountLabel.grid(row = 1, column = 0,  pady =0, sticky = 'n')

        self.billingVatableAmountLabel = Label(
            self.amountFrame, width = int(WR*12), text="", bg="#4A2727",font=('Helvetica',int(FR*22),'bold'), fg='#FAF712')
        self.billingVatableAmountLabel.grid(row=1, column=1, sticky="n",  pady=0)
        self.billingVatableAmountLabel.config(text=self.billingTotalAmount)
       
        #total amount
        self.totalAmountLabel = Label(
            self.amountFrame, width = int(WR*10), text='Grand Total :',font=('Helvetica',int(FR*22),'bold'), bg='#4A2727', fg='#FAF712')
        self.totalAmountLabel.grid(row = 2, column = 0,  pady =2, sticky = 'n')

        self.billingAmountLabel = Label(
            self.amountFrame, width = int(WR*12), text="", bg="#4A2727", font=('Helvetica',int(FR*22),'bold'), fg='#FAF712')
        self.billingAmountLabel.grid(row=2, column=1, sticky="n",  pady=2)
        self.billingAmountLabel.config(text=self.billingTotalAmount)

        #print receipt
        # self.printreceipt= Button(self.billingFrame,text="Print Receipt",bg="#7ee081",width=10)
        # self.printreceipt.grid(row=9,column=4,pady=10,ipadx=20)



    ## End of GUI        lbl.pack()

    ## End of GUI

    ## Supporting Functions

    #Gets Date and time from system and initialize self.(date/time)
    def getDateTime(self):
        nw = datetime.now()
        date = nw.strftime("%d/%m/%Y")
        time = nw.strftime("%H:%M")
        return (date,time)



    ## End of Supporting Functions


    ## Data processing Functions

    #Gets the data from the self.displayLabel -> creates json data -> post data to cloud
    def fetchRecord(self):
        self.widgetValue = []
        self.widgetlabel = []
        print(" Captured")
        for widget in self.displayLabel.winfo_children():
            print(widget.winfo_class())
            if(widget.winfo_class()== "TLabel"):
                self.widgetlabel.append(widget.cget("text"))
            elif (widget.winfo_class() == "Entry"):
                 self.widgetValue.append(widget.get())
            elif (widget.winfo_class()== "TCombobox") :
                 self.widgetValue.append(widget.get())
            elif (widget.winfo_class()== "Text") :
                 self.widgetValue.append(widget.get(1.0,'end-1c'))
            else:
                continue

        self.capturedRecord = dict(zip(self.widgetlabel,self.widgetValue))
        return self.capturedRecord

    def createRecord(self):
        self.rawData = self.fetchRecord()
        print(self.rawData)
        try:
            for x in self.widgetValue:
                if (x == ''):
                    raise ValueError
            self.postRecord()
        except ValueError:
            messagebox.showwarning("Insufficient Record", "All Fields Required")

    ## End of Data Processing Functions

    ## Database updating functions
    def postRecord(self):
        self.capturedRecord = self.rawData
        print("Captured Data: ")
        print(self.capturedRecord)


        # print("Connecting to firebase...")
        # fb = firebase.FirebaseApplication("https://expensedb-24f43.firebaseio.com/",None)
        # print("Posting data to firebase...")
        # self.firebasePostResult = fb.post('/expensedb-24f43/expenses',self.capturedRecord)
        # print("Data Posting Successful.")
        # print(" Document header id: ")
        # print( self.firebasePostResult)
        # print("Connecting to localhost:27017..")
        # print("Posting Data to localhost:27017.. ")

        ######### uncomment this line for local storage
        connection = pymongo.MongoClient("localhost",27017)
        database = connection['saiRecords']
        collection = database['inventory']

        ## for cloud atlas
        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.inventory
        try:
            validate = collection.find_one({'Product Name': self.rawData['Product Name']},{'_id':1}) 
            
            if (validate != None):
                raise ValueError

            try:
                self.rawData['Quantity'] = float(self.rawData['Quantity'])
                self.rawData['Sales Price'] = float(self.rawData['Sales Price'])
                self.rawData['Cost Price'] = float(self.rawData['Cost Price'])
                self.rawData['Order'] = 0
                self.rawData['Sold'] = 0

                collection.insert_one(self.rawData)
                print("Data Posting Completed")
                # connection.close()
                messagebox.showinfo("Information", "Product Addition Successful")
                self.addNewRecord()
            except ValueError:
                messagebox.showerror("Value Error", "Quantity and Unit Cost must be a Number.")

            
        except ValueError:
            messagebox.showwarning('Request Denied', 'Product with same name is available in Inventory.')
     #Frame and gui for view tab

    def navigationFrame_view(self, tab):
        self.displayFrame = Frame(tab)
        self.displayFrame.pack(fill = 'both')

        self.belowFrame = Frame(tab, bg="#d1eded")
        self.belowFrame.pack(fill=X, side="bottom")

        self.billdisplayFrame = Frame(self.displayFrame)
        self.billdisplayFrame.pack(side = 'left', padx = 10, pady = 10)

        self.buttonFrame = Frame(self.displayFrame)
        self.buttonFrame.pack(side = 'left', fill = 'y')
        
        self.searchLabelFrame = Frame(self.billdisplayFrame)
        self.searchLabelFrame.pack(pady = 10)

        searchhelpFrame = Frame(self.searchLabelFrame)
        searchhelpFrame.pack( side = 'left', pady = 10)
        #GUI of view tab
        
        listboxFrame = Frame (self.billdisplayFrame)
        listboxFrame.pack(pady = 10, padx = 5)

        self.labelsearchby = Label(searchhelpFrame, text="Search By", font=('Comic Sans MS', int(FR*15), 'bold'))
        self.labelsearchby.grid(padx = 5)
        helpLabel = Label(self.searchLabelFrame, text='(Set Search filter)', font =('Comic Snas MS', int(FR*12) ))
        helpLabel.pack(side='bottom')
        
        def printBill():
            try:
                billIndex = itemlistbox_view.index(ANCHOR)
                billId = self.view_productId[billIndex]
                
                ##For Cloud Atlas
                # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                # db = client.get_database('saiRecords')
                # collection = db.sales
                
                ##For Local Database Storage
                connection = pymongo.MongoClient("localhost", 27017)
                database = connection['saiRecords']
                collection = database['sales']

                data = collection.find_one({'_id': ObjectId(billId)}) 
                connection.close()
                print(data)
                count = 0
                for rows in view_viewTree.get_children():
                    view_viewTree.delete(rows)
                
                dateLabel.config(text= data['Date'])
                customerNameLabel.config(text=data['Customer Name'])
                timeLabel.config(text=data['Time'])
                billTotalLabel.config(text=data['Grand Total'])
                

                for vlue in (data['Products']):
                    print(vlue)
                    if "?" in vlue:
                        print('inside  if statement')
                        processed_name=vlue.replace('?','.')
                    else:
                        print('inside else statement')
                        processed_name=vlue
                    print(data['Products'][vlue]['iid'])
                    print()
                    view_viewTree.insert(parent='', index=END,
                                         iid=(data['Products'][vlue]['iid']), text=(count+1), values=(processed_name,
                                         data['Products'][vlue]['Quantity'],
                                         data['Products'][vlue]['Sales Price'],
                                         data['Products'][vlue]['Product Total']))
                    # view_viewTree.insert(parent='', index=END,
                    #  iid=(data['Products'][vlue]['iid']),text=(count+1),values=(processed_name,
                    #  data['Products'][vlue]['Quantity'],
                    #  data['Products'][vlue]['Per Unit Cost'],
                    #  data['Products'][vlue]['Sales Price'],
                    #  data['Products'][vlue]['Product Total']
                    # ))
                    count+=1
                helloat.config(text=data['Contact Number'])
            except (AttributeError, IndexError):
                messagebox.showerror('Invalid Request', 'Bill Selection Required')
            except KeyError:
                helloat.config(text='N/A')
            
            
        def setSearchTips(event):
            key = viewcombobox_search.get()
            if (key == 'Date'):
                helpLabel.config(text='(Search Format: DD/MM/YYYY)')
            else:
                helpLabel.config(text='(Search Format: Name)')

        def displayBillSearch(event=''):
            example = []
            self.view_productId = []
            searchValue = billSearchEntry.get()
            key = viewcombobox_search.get()
            try:
                itemlistbox_view.delete(0, END)
                if (key == ""):
                    raise ValueError
                else:
                    if (key == 'Date'):
                        searchFilter = '/123/'
                        helpLabel.config(text = "(Search Format : DD/MM/YYYY)")
                    else:
                        searchFilter = 'i'
                        helpLabel.config(text='(Search Format : Name)')
                    #For Local database Storage
                    connection = pymongo.MongoClient("localhost", 27017)
                    database = connection['saiRecords']
                    collection = database['sales']

                    ##For Cloud Atlas
                    # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                    # db = client.get_database('saiRecords')
                    # collection = db.sales
                    
                    result = collection.find({key: {'$regex': searchValue, '$options': searchFilter}})
                    connection.close()
                    for x in result:
                        example.append(x['Customer Name'] + ' ------  ' + x['Date'] + '------' +  x['Contact Number'])
                        self.view_productId.append(x['_id'])
                        
                    itemlistbox_view.insert(0, *example)
                    # if (len(self.view_productId) < 1):
                    #     messagebox.showinfo("Search Request", "No Record Found")
                    
            except ValueError:
                messagebox.showerror("Invalid Request", "Set Search Filter")
                
            
        viewcombobox_search = ttk.Combobox(
            self.searchLabelFrame, textvariable=4, width = int(WR*12), font = ('Comic Sans MS', int(FR*15)), state = 'readonly')
        viewcombobox_search['values'] = (
            'Date',
            'Customer Name',
        )
        viewcombobox_search.current(0)
        

        viewcombobox_search.pack(side='left', padx=5)
        viewcombobox_search.bind('<<ComboboxSelected>>',setSearchTips)

        #for search bar
        billSearchEntry = Entry(self.searchLabelFrame, width = int(WR*38), font =('Comic Snas MS', int(FR*20) ))
        billSearchEntry.pack(side='left')
        billSearchEntry.bind('<KeyRelease>', displayBillSearch)
        billSearchEntry.bind('<Return>', )


        #search button button
        # viewSearch_btn = Button(self.searchLabelFrame, text="Search",
        #                         width = int(WR*10), bg="#6aeb7b", command=displayBillSearch)
        # viewSearch_btn.pack(side='left')

        
        #for listbox
        itemlistbox_view = Listbox(listboxFrame, width = int(WR*60), height = int(HR*4), bg="#e8eddf", font =('Comic Snas MS', int(FR*15) ))
        itemlistbox_view.grid(column=0, row=0, columnspan=1)
        

        #for scroll bar
        viewScrollbar = Scrollbar(listboxFrame, orient=VERTICAL)
        viewScrollbar.config(command=itemlistbox_view.yview)
        viewScrollbar.grid(row=0, ipadx=5, column=5, sticky='ns')

        informationFrame = Frame(self.billdisplayFrame)
        informationFrame.pack(pady = 5)
        #bill details label 

        lbl = Label(informationFrame, text = "Bill Details", font = ('Comic Snas MS ', int(FR*15), 'bold', 'underline'))
        lbl.grid(row = 0, column = 0, columnspan = 4)
        #date label
        Viewdatelabel = Label(informationFrame, text='Date : ', font = ('Helvetica', int(FR*12)))
        Viewdatelabel.grid(row=1, column=0)
        
        dateLabel = Label(informationFrame, text='--/--/----', font=('Comic Sans MS', int(FR*15), 'bold'))
        dateLabel.grid(row=1, column=1)

        #custumer name label
        Viewcustumername = Label(
            informationFrame, text='Customer Name: ', font=('Hevetica', int(FR*12)))
        Viewcustumername.grid(row=1, column=2)

        customerNameLabel = Label(
            informationFrame, text='---------', font=('Comic Sans MS', int(FR*12), 'bold'))
        customerNameLabel.grid(row=1, column=3)

        ViewTime = Label(informationFrame, text='Time:', font=('Hevetica', int(FR*12)))
        ViewTime.grid(row=2, column=0)

        timeLabel = Label(informationFrame, text='--:-- --',font=('Comic Snas MS', int(FR*12), 'bold'))
        timeLabel.grid(row=2, column=1, padx = 10)

        helloatLabel = Label(informationFrame, text = 'Contact Number', font=('Hevetica', int(FR*12)))
        helloatLabel.grid(row = 1, column = 4)

        helloat = Label (informationFrame, text = ' ----------- ', font = ('Comic Sans MS', int(FR*10), 'bold'))
        helloat.grid(row= 1, column=5)

        #Bill Total Labels 
        billTotal = Label(informationFrame, text='Bill Total ', font = ('Helvetica',int(FR*15),'bold'))
        billTotal.grid(row=2, column=2,padx = 20)

        billTotalLabel = Label(informationFrame, text='------ /-', bg='#F2F81D', fg='#164ECF', font=('Helvetica', int(FR*15), 'bold'))
        billTotalLabel.grid(row = 2, column = 3)

        billFrame = Frame(self.billdisplayFrame)
        billFrame.pack()

        view_viewTree = ttk.Treeview(billFrame,height = int(HR*10), style="mystyle.Treeview")

        #Define Columns
        view_viewTree['columns'] = ('Product Name',  'Quantity','Sales Price','Product Total')
        view_viewTree.column('#0', width = int(WR*60), minwidth=25, anchor=CENTER)
        view_viewTree.column('Product Name', width = int(WR*425), anchor=W)
        view_viewTree.column('Sales Price', width = int(WR*150), anchor=CENTER)
        view_viewTree.column('Quantity', width = int(WR*150), anchor=CENTER)
        view_viewTree.column('Product Total', width = int(WR*150), anchor=CENTER)


        #Create Headings
        view_viewTree.heading('#0', text='S.N', anchor=CENTER)
        view_viewTree.heading('Product Name', text='Product Name', anchor=W)
        view_viewTree.heading('Sales Price', text='Sales Price', anchor=CENTER)
        view_viewTree.heading('Quantity', text='Quantity', anchor=CENTER)
        view_viewTree.heading('Product Total', text='Product Total', anchor=CENTER)
        view_viewTree.pack(side='left', padx = 15)
        Treescrollbar = Scrollbar(billFrame, orient=VERTICAL)
        Treescrollbar.config(command=view_viewTree.yview )
        Treescrollbar.pack(side='left' , fill= 'y')

        def searchSale():

            pass

        def customerCopy():
            billIndex = itemlistbox_view.index(ANCHOR)
            billId = self.view_productId[billIndex]

            ##For Local Database Storage
            connection = pymongo.MongoClient("localhost", 27017)
            database = connection['saiRecords']
            collection = database['sales']

            ##For Cloud Atlas
            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database('saiRecords')
            # collection = db.sales



            data = collection.find_one({'_id': ObjectId(billId)})
            connection.close()

            # Creating Canvas
            c = canvas.Canvas("bill.pdf", pagesize=(595,800), bottomup=0)
            # logo=('./res/logo.jpg')
            # c.drawImage(logo,10,10,height = int(HR*20),width=20)
            c.setFont("Helvetica-Bold", 20)
            c.drawCentredString(298, 60, "Regmi Electricals Center")
            c.setFont("Helvetica-Bold", 15)
            c.drawCentredString(298, 80, "Jaljala-03,Beni")
            c.drawCentredString(298, 100, "Parbat,Nepal")
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(500, 100, "Contact Number: 069-520747 ")
            c.drawCentredString(543, 110, " 9857621604 ")
            c.drawCentredString(50, 100, "PAN-301155407")
            c.line(10,120,790,120)
            # c.setFont('Times-Bold', 20)
            # c.drawCentredString(298, 140, "Bill Invoice ")
            c.setFont('Helvetica', 15)
            c.drawString(15, 170, "Date : ")
            c.drawString(65, 170, data['Date'])
            c.drawString(15, 200, "Customer Name: ")
            c.drawString(140, 200, data['Customer Name'])
            c.setFont('Courier-Bold', 12)
            c.drawString(15,230,"S.N")
            c.drawString(110, 230, "Product Name")
            c.drawString(350, 230, "Unit Cost")
            c.drawString(430, 230, "Qunatity") 
            # c.drawString(430, 230, "Discount")
            c.drawString(520, 230, "Total")
            c.line(10,235,790,235)
            c.setFont('Times-Roman', 12)

            cnt = 1
            x=16
            y = 250
            for items in data['Products']:
                c.drawString(x, y, str(cnt))
                name=''
                if '?' in items:
                    name = items.replace('?','.')
                else:
                    name=items
                c.drawString(x+50, y, name)
                qty = str(data['Products'][items]['Quantity'])
                
                # print(data)
                c.drawCentredString(x+360, y, str(data['Products'][items]['Sales Price']))  #x+345 
                c.drawCentredString(x+445, y, qty)
                c.drawCentredString(x+520, y, str(data['Products'][items]['Product Total']))
                cnt+=1
                y+=20
            
            c.line(10,y,790,y)
            c.setFont('Courier-Bold', 20)
            c.drawCentredString(200, y+20, "Grand Total")
            c.drawCentredString(500,y+20, str(data['Grand Total']))
            c.setFont('Courier-Bold', 50)
            c.setFillAlpha(0.2)
            c.rotate(-45)
            c.drawCentredString(-100, 500, "Customer Copy")
            c.rotate(45)
            c.setFillAlpha(1)
            c.line(20, 700, 220, 700)
            c.line(400, 700, 570, 700)
            c.setFont("Helvetica", 20)
            c.drawCentredString(120, 720, "Authorized Signature")
            c.drawCentredString(490, 720, "Store Seal")
            c.line(20,750,570,750)
            c.showPage()
            try:
                c.save()
                wb.open_new('bill.pdf')
            except PermissionError:
                messagebox.showerror("Permission Denied","The bill is currently open. Please close the file to display new bill.")

        #Button Frame GUI 

        dspbill = Button(self.buttonFrame,text="Display Bill", command=printBill, font = ('Helvetica', int(FR*15),'bold'))
        dspbill.pack(side="top",pady = 10)

        prntBill = Button(self.buttonFrame, text = "Print Bill", command=customerCopy, width = int(WR*15),font = ('Helvetica', int(FR*15),'bold'))
        prntBill.pack(side = "top", pady = 10)

       


        # sendBill = Button(self.buttonFrame, text = "Send Bill")
        # sendBill.pack(pady= 10 )

        
    def navigationFrame_settings(self,tab):
        # self.displayFrame.destroy()
        self.displayFrame = Frame(tab)
        self.displayFrame.pack(fill="both", padx=20, pady=20)

        def configureSettingsData(key,value):
            self.UpdatePopUp.destroy()

            ##For local Database storage
            connection = pymongo.MongoClient('localhost',27017)
            dbs = connection['saiRecords']
            collection = dbs['configuration']

            ##For Cloud Atlas
            # client = MongoClient(
            #     "mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database('saiRecords')
            # collection = db.configuration

            
            collection.find_one_and_update({'_id': 'settingsData'},{'$set':{key:value}})
            data = collection.find_one({'_id':'settingsData'})
            self.sender_emaildata.config(text = data['sender_email'])
            self.receiver_emaildata.config(text = data['receiver_email'])
            self.master_passworddata.config(text=data['master_password'])
            self.sender_passworddata.config(text=data['sender_password'])
            
            messagebox.showinfo('Value Updated','Value has been successfully Updated')


        # Functions to Update Values in the Database
        def update_sender():
            value = self.AppsSettingsEntry.get()
            configureSettingsData('sender_email', value)
        
        def update_receiver():
            value = self.AppsSettingsEntry.get()
            configureSettingsData('receiver_email', value)
        
        def update_senderPassword():
            value = self.AppsSettingsEntry.get()
            configureSettingsData('sender_password', value)
        def update_MasterPassword():
            value = self.AppsSettingsEntry.get()
            print('Flag3')
            configureSettingsData('master_password', value)

        #Displays pop-Up to get new Values
        def displayTop(displayText,cmd):
            self.UpdatePopUp = Toplevel()
            self.UpdatePopUp.grab_set()
            self.UpdatePopUp.title("Update Values")
            
            self.UpdatePopUp.geometry("+%d+%d" % (400, 300))
            # self.UpdatePopUp.minsize(200,200)

            updateLabel = Label(self.UpdatePopUp, text=displayText)
            updateLabel.grid(row = 0, column = 0,padx=10, pady=10)
            self.AppsSettingsEntry = Entry(self.UpdatePopUp, width=20)
            self.AppsSettingsEntry.grid(row = 1, column = 0,padx=10, pady=10)
            self.AppsSettingsEntry.focus()
            print("Flag1")
            updateBtn = Button(self.UpdatePopUp, text="Update Value", command=cmd)
            updateBtn.grid(row=2, column=0, padx=10, pady=20)
            
            

        # # Functions to Display pop up and get new values
        def getNewSender():
            displayTop('Enter New Sender Mmail-id',update_sender)
            
        def getNewSenderPassword():
            displayTop('Enter New Sender Password', update_senderPassword)

        def getNewReceiver():
            displayTop('Enter New Receiver Mail-id', update_receiver)

        def getMasterPassword():
            print('Flag2')
            displayTop('Enter New Master Password', update_MasterPassword)

        #Displays content in the App Settings Tab after authentyication
        def displayContents():
            try:

                ##For local database storage
                connection = pymongo.MongoClient('localhost',27017)
                dbs = connection['saiRecords']
                collection = dbs['configuration']

                #For Cloud Atlas
                # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                # db = client.get_database('saiRecords')
                # collection = db.configuration

                sysData=collection.find_one({'_id': 'settingsData'})
                print(sysData)
                connection.close()
                receiverLabel = Label(self.displayFrame, text = " Send mail using :", font = ('Helvetica', int(FR*10),'bold'))
                receiverLabel.grid(row=0, column=0, padx=10, pady=10, sticky='w')
                
                infoLabel = Label(self.displayFrame, text=" (Set this email address send backup)")
                infoLabel.grid(row=1, column=0, columnspan=2,padx=10, pady=0, sticky='w')

                self.sender_emaildata = Label(self.displayFrame, text=sysData['sender_email'], font=('Helvetica', int(FR*10), 'bold'))
                self.sender_emaildata.grid(row = 0, column = 1, padx = 10, pady = 10)

                senderPasswordLabel = Label(self.displayFrame, text = " Sender email password :",font = ('Helvetica', int(FR*10),'bold'))
                senderPasswordLabel.grid(
                    row=2, column=0, padx=10, pady=10, sticky='w')

                infoLabel = Label(self.displayFrame, text=" (Password of the sender's email address)")
                infoLabel.grid(row=3, column=0, columnspan=2,
                            padx=10, pady=0, sticky='w')

                self.sender_passworddata = Label(self.displayFrame, text='*********', font=('Helvetica', int(FR*10), 'bold'))#sysData['sender_password']
                self.sender_passworddata.grid(row=2, column=1, padx=10, pady=10)

                receiverLabel = Label(self.displayFrame, text= " Receive mail in: ", font = ('Helvetica', int(FR*10), 'bold'))
                receiverLabel.grid(row=4, column=0, padx=10, pady=10, sticky='w')

                infoLabel = Label(self.displayFrame, text=" (Set this email address to receive backup)")
                infoLabel.grid(row = 5, column = 0,columnspan = 2, padx = 10, pady = 0, sticky='w')

                self.receiver_emaildata = Label(self.displayFrame, text = sysData['sender_email'],font = ('Helvetica', int(FR*10),'bold'))
                self.receiver_emaildata.grid(row = 4, column = 1, padx = 10, pady = 10)
                
                masterPasswordLabel = Label(self.displayFrame, text = "Master Password :",font = ('Helvetica', int(FR*10),'bold'))
                masterPasswordLabel.grid(
                    row=6, column=0, padx=10, pady=10, sticky='w')

                infoLabel = Label(self.displayFrame,text=" (Password to access the Setting Tab)")
                infoLabel.grid(row=7, column=0, columnspan=2,
                            padx=10, pady=0, sticky='w')
                
                self.master_passworddata = Label(self.displayFrame, text=sysData['master_password'], font=('Helvetica', int(FR*10), 'bold'))
                self.master_passworddata.grid(row = 6, column = 1, padx = 10, pady = 10)

                upd_btn=ttk.Style()
                upd_btn.configure('Update.TButton',width = int(WR*10), font=('Times New Roman',int(FR*10)))

                upd_sendermail = ttk.Button(self.displayFrame, text ="Update", style = 'Update.TButton', command =getNewSender)
                upd_sendermail.grid(row =0 , column =2 )

                upd_mailPassword = ttk.Button(self.displayFrame, text="Update", style='Update.TButton', command=getNewSenderPassword)
                upd_mailPassword.grid(row = 2, column =2 )
                upd_receiverMail = ttk.Button(self.displayFrame, text="Update", style='Update.TButton', command=getNewReceiver)
                upd_receiverMail.grid(row=4, column=2)
                print('Flag1')
                upd_masterPassword = ttk.Button(self.displayFrame, text="Update", style='Update.TButton', command=getMasterPassword)
                upd_masterPassword.grid(row=6, column=2)


            except TypeError:
                pass
        displayContents()
    
    def navigationFrame_customerDetails(self, tab):
        buttonBg = "#284F9B"
        self.buttonFrame = Frame(tab, bg=buttonBg)
        self.buttonFrame.pack(fill=Y, side="left")

        self.belowFrame = Frame(tab, bg="#d1eded")
        self.belowFrame.pack(fill=X, side="bottom")

        # self.customerDisplay.destroy()
        #Frame for left 
        self.customerDisplay = Frame(tab, bg='#FFFFFF')
        self.customerDisplay.pack(fill="both", side="left")

        #Frame for right
        self.customerBillDisplay = Frame(tab, bg='#FFFFFF')
        self.customerBillDisplay.pack(fill="both", side="left")

        #Top Frame inside Left Frame
        self.customerDisplay_top = Frame(self.customerDisplay, bg = '#ffffff')
        self.customerDisplay_top.pack(fill = 'both', padx= 10)

        #Bottom Frame inside Left Frame
        self.customerDisplay_dwn = Frame(self.customerDisplay, bg='#ffffff')
        self.customerDisplay_dwn.pack(fill='both', padx=10, pady = 10)
        
        def customerHistory():

            def displayBill():
                index = billList.index(ANCHOR)
                print(index)
                print(self.billpointer[index])
                connection = pymongo.MongoClient("localhost", 27017)
                database = connection['saiRecords']
                if 'Sales' in self.name_list[index]:
                    Collection= database['sales']
                else:
                    Collection= database['order']
                bill=Collection.find_one({'_id':self.billpointer[index]})
                print(bill)
                dateLabel.config(text=bill['Date'])
                timeLabel.config(text=bill['Time'])
                customerNameLabel.config(text=bill['Customer Name'])
                helloat.config(text=bill['Contact Number'])
                billTotalLabel.config(text=bill['Grand Total'])

                count=0
                for rows in view_viewTree.get_children():
                    view_viewTree.delete(rows)


                for vlue in (bill['Products']):
                    print(vlue)
                    if "?" in vlue:
                        print('inside  if statement')
                        processed_name=vlue.replace('?','.')
                    else:
                        print('inside else statement')
                        processed_name=vlue
                        view_viewTree.insert(parent='', index=END,
                                         iid=(bill['Products'][vlue]['iid']), text=(count+1), values=( processed_name ,
                                         bill['Products'][vlue]['Quantity'],
                                         bill['Products'][vlue]['Sales Price'],
                                         bill['Products'][vlue]['Product Total']))


                

                

            def searchCustomer():
                name = ent_name.get()
                number = ent_phone.get()
                connection = pymongo.MongoClient("localhost", 27017)
                database = connection['saiRecords']
                collection = database['sales']
                billList.delete(0, END)

                self.name_list = []
                self.billpointer= []
                totalPurchase = 0
                result = collection.find({'Customer Name':{'$regex': name, '$options': 'i' } , 'Contact Number': number})
                
                print("List of Object ID")
                for x in result:
                        totalPurchase+=x['Grand Total']
                        self.name_list.append(
                            x['Customer Name'] +  '------' + x['Date'] + '---' + 'Sales')
                        self.billpointer.append(x['_id'])
                        # self.view_productId.append(x['_id'])
                collection = database['order']
                result = collection.find({'Customer Name':{'$regex': name, '$options': 'i' } , 'Contact Number': number})
                for x in result:
                    totalPurchase+=x['Grand Total']
                    self.name_list.append(
                        x['Customer Name'] +  '------' + x['Date'] + '---' + 'Order')
                    self.billpointer.append(x['_id'])

                billList.insert(0, *self.name_list)
                salesTotal.config(text = totalPurchase)

            
                
            
            lbl_name = Label(self.customerDisplay_top, text = "Name", bg='white', font=('Hevetica', int(FR*14), 'bold'))
            lbl_name.grid(row = 0, column = 0, pady=20)

            ent_name = Entry(self.customerDisplay_top, font=("Helvetica", int(FR*15), 'bold'))
            ent_name.grid(row=0,column=1)

            lbl_phone = Label(self.customerDisplay_top, text="Contact Number",bg ='white', font=('Hevetica', int(FR*14), 'bold'))
            lbl_phone.grid(row=1, column=0)

            ent_phone = Entry(self.customerDisplay_top,
                              font=("Helvetica", int(FR*15), 'bold'))
            ent_phone.grid(row=1, column=1)

            btn_search = Button(self.customerDisplay_top, text = 'Search', command = searchCustomer, bg = '#3399ff', fg = '#ffffff', border = 0, font = ('Comic San MS', int(FR*12),'bold'))
            btn_search.grid(row=2, column= 1, padx= 10)

            salesTotalLabel = Label(self.customerDisplay_top, bg='#ffffff', text='Total Purchase',
                                    fg='#164ECF', font=('Helvetica', int(FR*14), 'bold'))
            salesTotalLabel.grid(row=3, column=0, pady=10)

            salesTotal = Label(self.customerDisplay_top, text='------ /-',
                           bg='#F2F81D', fg='#164ECF', font=('Helvetica', int(FR*14), 'bold'))
            salesTotal.grid(row=3, column=1, pady=10)

            lbl_BillDetails = Label(self.customerDisplay_dwn, text='Bill Records', font=('Comic Sans MS', int(FR*10), 'bold'))
            lbl_BillDetails.grid(row=0, column=0, columnspan=3 )

            billList  = Listbox(self.customerDisplay_dwn, bg = '#ffffff', selectmode='Single', heigh=14, width = int(WR*38), font=('Helvetica', int(FR*12), 'bold'))
            billList.grid(row=1, column=0, pady=20)

            viewScrollbar = Scrollbar(self.customerDisplay_dwn, orient=VERTICAL)
            viewScrollbar.config(command=billList.yview)
            viewScrollbar.grid(row=1, ipadx=1, column=1, sticky='ns')

            btn_dsp = Button(self.customerDisplay_dwn, text = 'Display', command=displayBill, font=('Helvetica',int(FR*15),'bold'))
            btn_dsp.grid(row=2, column= 0)

            #GUI for Right frame

            


        s_btn = ttk.Style()
        s_btn.configure('TButton', height = int(HR*3), width = int(WR*20), border=0,
                        background=buttonBg,
                        font=("Helvetica", int(FR*14), 'bold'))
        s_btn.map('TButton',
                  foreground=[('disabled', 'yellow'),
                              ('pressed', 'red'),
                              ('active', '#5A63F5')],
                  background=[('disabled', 'magenta'),
                              ('pressed', '!focus', 'cyan'),
                              ('active', 'green')],

                  )
        lbl = Label(self.customerBillDisplay, text="Bill Details", bg = '#ffffff', font = ('Comic Snas MS ', 15, 'bold', 'underline'))
        lbl.grid(row=0, column=0, columnspan=4)
        #date label
        Viewdatelabel = Label(
            self.customerBillDisplay, bg='#ffffff', text='Date : ', font=('Helvetica', int(FR*12)))
        Viewdatelabel.grid(row=1, column=0)

        dateLabel = Label(self.customerBillDisplay, text='--/--/----',
                          font=('Comic Sans MS', int(FR*15), 'bold'))
        dateLabel.grid(row=1, column=1)

        #custumer name label
        Viewcustumername = Label(
            self.customerBillDisplay, bg='#ffffff', text='Customer Name: ', font=('Hevetica', int(FR*12)))
        Viewcustumername.grid(row=3, column=0)

        customerNameLabel = Label(
            self.customerBillDisplay, bg='#ffffff', text='---------', font=('Comic Sans MS', int(FR*12), 'bold'))
        customerNameLabel.grid(row=3, column=1)

        ViewTime = Label(self.customerBillDisplay, bg = '#ffffff', text='Time:', font=('Hevetica', int(FR*12)))
        ViewTime.grid(row=2, column=0)

        timeLabel = Label(self.customerBillDisplay, bg='#ffffff', text='--:-- --',
                          font=('Comic Snas MS', int(FR*12), 'bold'))
        timeLabel.grid(row=2, column=1, padx=10)

        helloatLabel = Label(
            self.customerBillDisplay, bg = '#ffffff', text='Contact Number', font=('Hevetica', int(FR*12)))
        helloatLabel.grid(row=4, column=0)

        helloat = Label(self.customerBillDisplay, bg='#ffffff', text=' ----------- ',
                        font=('Comic Sans MS', int(FR*10), 'bold'))
        helloat.grid(row=4, column=1)

        #Bill Total Labels
        billTotal = Label(self.customerBillDisplay, bg='#ffffff', text='Bill Total ',
                          font=('Helvetica', int(FR*15), 'bold'))
        billTotal.grid(row=5, column=0, padx=20)

        billTotalLabel = Label(self.customerBillDisplay,  text='------ /-',
                               bg='#F2F81D', fg='#164ECF', font=('Helvetica', int(FR*15), 'bold'))
        billTotalLabel.grid(row=5, column=1, pady = 10)

        

        billFrame = Frame(self.customerBillDisplay)
        billFrame.grid(row = 7, column = 0, columnspan=4)

        view_viewTree = ttk.Treeview(
            billFrame, height = int(HR*10), style="mystyle.Treeview")

        #Define Columns
        view_viewTree['columns'] = (
            'Product Name',  'Quantity', 'Sales Price', 'Product Total')
        view_viewTree.column('#0', width = int(WR*60), minwidth=25, anchor=CENTER)
        view_viewTree.column('Product Name', width = int(WR*200), anchor=W)
        view_viewTree.column('Sales Price', width = int(WR*100), anchor=CENTER)
        view_viewTree.column('Quantity', width = int(WR*120), anchor=CENTER)
        view_viewTree.column('Product Total', width = int(WR*150), anchor=CENTER)

        #Create Headings
        view_viewTree.heading('#0', text='S.N', anchor=CENTER)
        view_viewTree.heading('Product Name', text='Product Name', anchor=W)
        view_viewTree.heading('Sales Price', text='Sales Price', anchor=CENTER)
        view_viewTree.heading('Quantity', text='Quantity', anchor=CENTER)
        view_viewTree.heading(
            'Product Total', text='Product Total', anchor=CENTER)
        view_viewTree.pack(side='left', padx=5)
        Treescrollbar = Scrollbar(billFrame, orient=VERTICAL)
        Treescrollbar.config(command=view_viewTree.yview)
        Treescrollbar.pack(side='left', fill='y')

        ##Gui for Left Navigation Button

        self.btn_details = ttk.Button(
            self.buttonFrame, text="Customer History", style='TButton', command=customerHistory)
        self.btn_details.grid(column=0, row=1, pady=10)

        customerHistory()


class AuthUser(Tk):
    def __init__(self):
        super(AuthUser, self).__init__()
        self.title("Login")
        self.iconbitmap('./res/dsk.ico')
        self.geometry('600x600')

        self.minsize(500,400)
        self.maxsize(550,450)
        

        displayFrame = Frame(self, bg='#ffffff')
        displayFrame.pack( fill='both')

        companyLabel = Label(displayFrame, text='Regmi Electricals Centre',
                             fg='#000000',bg = '#ffffff', font=('Helvetica',int(FR*25),'bold', 'underline'))
        companyLabel.pack(padx = 20,pady=5)


        detailsframe = Frame(displayFrame, bg='#ffffff')
        detailsframe.pack(pady = 20,padx = 20, fill = 'both')

        image = Image.open("./res/logo.jpg")
        test = ImageTk.PhotoImage(image)

        label1 = Label(detailsframe,image=test, width = int(WR*200), height = int(HR*200), bg = '#ffffff')
        label1.image = test
        label1.pack()

        

        def clearPlaceHolder(event):
            self.password_entry.delete(0, 'end')

        passwordFrame = Frame(detailsframe, bg = '#ffffff')
        passwordFrame.pack()

        image = Image.open('./res/lck.png')
        test = ImageTk.PhotoImage(image)
        locklbl = Label(passwordFrame, image=test, height = int(HR*50), width = int(WR*50), bg = '#ffffff' )
        locklbl.image = test
        locklbl.grid(row = 0, column = 0)

        self.password_entry = Entry(passwordFrame,border = 0,width = int(WR*15),font=('default',int(FR*12),), bg = '#f0f3f7')
        self.password_entry.grid(row = 0 , column = 1,padx = 2, pady = 10, sticky = 'w')
        self.password_entry.insert(0,"Enter Password")
        self.password_entry.bind('<FocusIn>', clearPlaceHolder)
        self.password_entry.bind('<Return>',self.checkPass)



        
        loginbutton = Button(detailsframe,text='Get Access', border = 0,width = int(WR*15),bg='#151FC4',fg = '#ffffff',font=('Helvetica',int(FR*13),'bold'), command = self.checkPass)
        loginbutton.pack(padx=10, pady = 10)
        loginbutton.bind("<Return>",self.checkPass)

        forgotPassword = Button(detailsframe, text='Forgot Password ?', cursor="hand2", border=0,
                                bg='#ffffff', fg='red', font=('Helvetica', int(FR*10), 'underline'), command=self.saendPassword)
        forgotPassword.pack(padx=10, pady = 10)

        ##For local storage
        connection = pymongo.MongoClient('localhost',27017)
        dbs = connection['saiRecords']
        collection = dbs['configuration']

        ##For Cloud Atlas
        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.configuration

        self.accessCred=collection.find_one({'_id': 'settingsData'})
        self.accessLoginKey = self.accessCred['master_password']
        connection.close()

    def checkPass(self,event=''):
        try:
            # fbase = firebase.FirebaseApplication("https://sales-and-inventory-85242-default-rtdb.firebaseio.com/", None)
            # giveAccess = fbase.get('/sales-and-inventory-85242-default-rtdb:/appAuthentication', '')
            accessStatus = 1  #;giveAccess['-MP5S3ILYqmOejEfu9Cp']['auth']
            if (accessStatus):
                key = self.password_entry.get()
                if (key == self.accessLoginKey):
                    self.destroy()
                    window = Window()
                    window.mainloop()
                else:
                    messagebox.showerror("Invalid Key", "Wrong Password. Please enter correct password")
            else:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Access Denied", "Your Lisence is expired. Please Contact Developer. ")
            self.destroy()
        except ConnectionError:
            messagebox.showwarning("Connection Error", "Active Internet connection is required to validate Lisence.")
            self.destroy()


    def saendPassword(self):
        try:
            nw = datetime.now()
            date = nw.strftime("%d/%m/%Y")
            time = nw.strftime("%H:%M")
            dte = date
            time = time
            validate = bool(0)
            validate = messagebox.askyesno(
                'Conformation Required', 'Do you want to send your password to the registered email address? ')
            if(validate):
                receiver_email = self.accessCred['receiver_email']
                password = self.accessCred['sender_password']
                sender_email = self.accessCred['sender_email']
                subject = "Access Key for the SaI Application "
                body = f' Kaligandaki Hardware \nYour Access Key is -  {self.accessLoginKey} \n Someone tried log in to the Software on {dte} at  {time} \n If this was not you, please consider conforming your staff'
                message = f'Subject: {subject}\n\n{body}'
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
                messagebox.showinfo("Access Key Sent", "The Access Key has been sent to the registered email address.")

                
        except smtplib.socket.gaierror:
            messagebox.showerror("Connection Failed", 'This function requires active internet connection.')
        
#authUser = AuthUser()
#authUser.mainloop()

window = Window()
window.mainloop()
