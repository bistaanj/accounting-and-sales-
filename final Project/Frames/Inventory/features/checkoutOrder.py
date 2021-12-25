from tkinter import *
from tkinter import ttk
import win32api
import pymongo
from Frames.supportingFunctions import warnUser
from config.dynamicSize import FR,WR,HR
import Frames.Billing.billingOptions as billingOptions

# creates frame and buttons inside the Billing tab's Navigation Button
def checkoutOrders(self):
    self.displayFrame.destroy()
    self.displayFrame = Frame(self.inventory,bg="#e8eddf")
    self.displayFrame.pack(fill="both")

    billingtypeFrame = Frame(self.displayFrame,bg='#e8eddf')
    billingtypeFrame.pack(fill='x')

    mainBillingFrame =Frame(self.displayFrame,bg='#e8eddf')
    mainBillingFrame.pack(side='left', fill='both', padx=20, pady=25, ipady=10)

    billingButtonFrame = Frame(self.displayFrame, bg = '#e8eddf')
    billingButtonFrame.pack(side = 'left', fill = 'both', pady = 15,ipady=10)
    # billingButtonFrame.grid(column=1, row=0, sticky=NS)

    billingSearchFrame=Frame(mainBillingFrame,bg='#e8eddf')
    billingSearchFrame.pack(padx= 30)
    # billingSearchFrame.grid(column = 0, row = 0, pady = 15)

    billingFrame = Frame(mainBillingFrame, bg='#e8eddf')
    billingFrame.pack( padx= 10, pady = 10)
    # billingFrame.grid(column = 0, row = 1, pady = 15)

    amountFrame = Frame(mainBillingFrame, bg='#e8eddf')
    amountFrame.pack(pady = 10)
    # amountFrame.grid(column = 0, row = 2)

    connection = pymongo.MongoClient("localhost", 27017)
    database = connection['saiRecords']
    collection = database['inventory']
    allProducts = collection.find()
    productDetails = {}
    for x in allProducts:
        if x['Order'] > 0:
            productDetails[x['Product Name']]= {'orderQuantity':x['Order'],'Sales Price':x['Sales Price']}
    #Displays Product in the Listbox of billing tabs to search for Product
    connection.close()
    
    def editOrder():
        def on_closing():
            top.destroy()
            self.executing = False

        def changeOrder(e=""):
            newOrderQuantity = askOrderQuantityEntry.get()
            if int(newOrderQuantity) == 0:
                deleteOrder(e)
            else:
                newSalesPrice = askSalesPriceEntry.get()
                productsInBill[product]['Quantity'] = newOrderQuantity
                productsInBill[product]['Sales Price']= newSalesPrice
                tAmout = int(newOrderQuantity)*float(newSalesPrice)
                productsInBill[product]['Product Total']= tAmout
                viewProductsInBill()
                # temp = viewTree.item(selected, 'values')
                # viewTree.item(selected,values=(temp[0],int(newOrderQuantity),temp[2],float(newSalesPrice),tAmout))
            top.destroy()
            self.executing = False

        def validateQuantity(e):
            try:
                if int(askOrderQuantityEntry.get()) > productDetails[product]['orderQuantity'] :
                    askOrderQuantityEntry.delete(-1,'end')
                    askOrderQuantityEntry.insert(0,int(productDetails[product]['orderQuantity']))
            except ValueError:
                askOrderQuantityEntry.delete(-1,'end')

        def validateSalesPrice(e):
            try:
                float(askSalesPriceEntry.get())
            except ValueError:
                askSalesPriceEntry.delete(-1,'end')

        iidEdit = viewTree.focus()
        if iidEdit =="":
            warnUser("Product sellection required.")
        else:
            product = (viewTree.item(iidEdit, 'values'))[0]
            top = Toplevel()
            self.executing = True
            top.grab_set()
            top.iconbitmap('./res/dsk.ico')
            top.geometry("+%d+%d" % (400, 400))

            availableOrderQuantity = Label(top, text="Ordered Quantity", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
            availableOrderQuantity.grid(row=0, column=0)

            askOrderQuantityEntry = Entry(top, width = int(WR*10), font=('Comic Sans MS', int(FR*15), 'bold'))
            askOrderQuantityEntry.insert(0,productDetails[product]['orderQuantity'])
            askOrderQuantityEntry.grid(row=0, column=1)
            askOrderQuantityEntry.bind("<KeyRelease>",validateQuantity)
            askOrderQuantityEntry.bind("<Return>",changeOrder)
            askOrderQuantityEntry.focus()
            salesPriceLbl = Label(top, text="Sales Price (RS)", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
            salesPriceLbl.grid(row = 1, column= 0)

            askSalesPriceEntry = Entry(top, width = int(WR*10), font=('Comic Sans MS', int(FR*15), 'bold'))
            askSalesPriceEntry.insert(0,productDetails[product]['Sales Price'])
            askSalesPriceEntry.grid(row=1, column=1)
            askSalesPriceEntry.bind("<KeyRelease>",validateSalesPrice)
            askSalesPriceEntry.bind("<Return>",changeOrder)

            okBtn = Button(top, text="Sell", padx=5,pady=10, width = int(WR*8),font=('Georgia', int(FR*10),'bold'),
            command=changeOrder)
            okBtn.grid(row=3, column=0)
            top.protocol("WM_DELETE_WINDOW", on_closing)

    def modifyTotalAmount():
        billingTotalAmount = 0
        for i in viewTree.get_children():
            billingTotalAmount += float(viewTree.set(i,4))
        billingVatableAmountLabel.config(text = int(billingTotalAmount))
        billingAmountLabel.config(text = int(billingTotalAmount+0.13*billingTotalAmount))
        self.executing = False 

    def deleteOrder(e=""):
            iidDelete = viewTree.focus()
            product = (viewTree.item(iidDelete, 'values'))[0]
            productsInBill.pop(product)
            viewProductsInBill()

    def clearBilling(e=""):
            productsInBill.clear()
            viewProductsInBill() 
    
    def displayProductOptions(event = ''):
        example = []
        searchValue = billingSearchEntry.get()

        ##For local storage
        for x in productDetails:
            if searchValue.upper() in x.upper():
                example.append(x)
        itemlistbox.delete(0,END)
        itemlistbox.insert(0, *example)
    
    def viewProductsInBill():
        count = 0
        for rows in viewTree.get_children():
            viewTree.delete(rows)

        for values in productsInBill:
            viewTree.insert(parent='', index=END, iid=(productsInBill[values]['iid']),
                            text=(count+1),
                            values=(values,
                        productsInBill[values]['Quantity'],
                        productsInBill[values]['Units'],
                        productsInBill[values]['Sales Price'],
                        productsInBill[values]['Product Total']
                        ))
            count += 1
        modifyTotalAmount()

    def addAllProduct():
        for i in productDetails:
            if i not in productsInBill:
                addProduct("",i)

    def addProduct(event = '',product = ""):
        def validateQuantity(e):
            try:
                if int(askOrderQuantityEntry.get()) > productDetails[product]['orderQuantity'] :
                    askOrderQuantityEntry.delete(-1,'end')
                    askOrderQuantityEntry.insert(0,int(productDetails[product]['orderQuantity']))
            except ValueError:
                askOrderQuantityEntry.delete(-1,'end')

        def validateSalesPrice(e):
            try:
                float(askSalesPriceEntry.get())
            except ValueError:
                askSalesPriceEntry.delete(-1,'end')

        def displayToBill(event = "",product=""):
            try:
                orderQuatity = int(askOrderQuantityEntry.get())
                salesPrice = float(askSalesPriceEntry.get())
                index = itemlistbox.index(ANCHOR)
                product = itemlistbox.get(index)                
                top.destroy()
            except:
                if product != "":
                    orderQuatity = int(productDetails[product]['orderQuantity'])
                    salesPrice = float(productDetails[product]['Sales Price'])
            
            productToBill = collection.find_one({'Product Name': product})
            if (productToBill['Product Name'] in productsInBill.keys()):
                self.executing = False
                warnUser("Product Already in Bill")
                print("Already in bill")
            else:
                productTotal = int(salesPrice)*orderQuatity
                productsInBill[productToBill['Product Name']] = {}
                productsInBill[productToBill['Product Name']]['Quantity'] = orderQuatity
                productsInBill[productToBill['Product Name']]['iid'] = productToBill['_id']
                productsInBill[productToBill['Product Name']]['Sales Price'] = salesPrice
                productsInBill[productToBill['Product Name']]['Units'] = productToBill['Units']
                productsInBill[productToBill['Product Name']]['Product Total'] = productTotal
                viewProductsInBill()

        def on_closing():
            top.destroy()
            self.executing = False

        state_left = win32api.GetKeyState(0x01)
        if state_left<0 and not self.executing and  product == "":
            index = itemlistbox.index(ANCHOR)
            product = itemlistbox.get(index)
            if product == "":
                warnUser("Product Selection required")
                return
            self.executing = True
            billingSearchEntry.focus()
            top = Toplevel()
            top.grab_set()
            top.iconbitmap('./res/dsk.ico')
            top.geometry("+%d+%d" % (400, 400))

            availableOrderQuantity = Label(top, text="Ordered Quantity", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
            availableOrderQuantity.grid(row=0, column=0)

            askOrderQuantityEntry = Entry(top, width = int(WR*10), font=('Comic Sans MS', int(FR*15), 'bold'))
            askOrderQuantityEntry.insert(0,productDetails[product]['orderQuantity'])
            askOrderQuantityEntry.grid(row=0, column=1)
            askOrderQuantityEntry.bind("<KeyRelease>",validateQuantity)

            salesPriceLbl = Label(top, text="Sales Price (RS)", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
            salesPriceLbl.grid(row = 1, column= 0)

            askSalesPriceEntry = Entry(top, width = int(WR*10), font=('Comic Sans MS', int(FR*15), 'bold'))
            askSalesPriceEntry.insert(0,productDetails[product]['Sales Price'])
            askSalesPriceEntry.grid(row=1, column=1)
            askSalesPriceEntry.bind("<KeyRelease>",validateSalesPrice)

            askOrderQuantityEntry.focus()

            okBtn = Button(top, text="Sell", padx=5,pady=10, width = int(WR*8),font=('Georgia', int(FR*10),'bold'),
            command=displayToBill)
            okBtn.grid(row=3, column=0)
            top.protocol("WM_DELETE_WINDOW", on_closing)
            top.bind('<Return>',displayToBill)

        else:
            if not self.executing:
                displayToBill("",product)
            else:
                return
    

    #Billing GUI starts here
    productsInBill = {}
    #for billing name
    billtypelabel = Label(billingtypeFrame, text="Checkout Orders",
        bg='#e8eddf', font=('Helvetica',int(FR*30),'bold','underline'),fg ="#5A63F5", border=0 )
    billtypelabel.pack(fill ="both",side="top")

    searchlabel = Label(billingSearchFrame, text="Product Name", font=('Helvetica', int(FR*12),'bold'),bg='#e8eddf')
    searchlabel.grid(column=0,row=1, padx = 15)
    #for search bar
    billingSearchEntry = Entry(billingSearchFrame,width = int(WR*35),font=('Helvetica', int(FR*20),'bold'), bg='#f7eeee')
    billingSearchEntry.grid(column = 1 , row = 1, padx = 15)
    billingSearchEntry.bind('<KeyRelease>',displayProductOptions)


    #add button button
    addAllProduct = Button(billingSearchFrame, text="Add All Product", font = ('Helvetica', int(FR*12), 'bold'), width = int(WR*12), bg="#6aeb7b",command=addAllProduct)
    addAllProduct.grid(column = 5, row = 1)

    #for listbox
    itemlistbox = Listbox(
        billingSearchFrame, width = int(WR*80), height = int(HR*5), bg="#e8eddf")
    itemlistbox.grid(column=1,row=2,columnspan=4,pady=0)
    itemlistbox.bind("<<ListboxSelect>>", addProduct)



    #for scroll bar
    scrollbar = Scrollbar(billingSearchFrame, orient=VERTICAL)
    scrollbar.config(command=itemlistbox.yview)
    scrollbar.grid(row=2,ipadx=10,column=5,sticky='ns')


    #treeview Styling
    vtStyle = ttk.Style()
    vtStyle.configure('Treeview.Heading', font=('Comic Sans MS', int(FR*12), 'bold'))
    treeStyle=ttk.Style()

    treeStyle.configure("mystyle.Treeview", highlightthickness=1, bd = 0,rowheight = int(HR*25), font=('Georgia', int(FR*13)))
    # treeStyle.layout('mystyle.Treeview',[('mystyle.Treeview.treearea',{'sticky':'nswe'})])

    #treeview
    viewTree = ttk.Treeview(billingFrame, height = int(HR*10), style="mystyle.Treeview")
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
    Treescrollbar = Scrollbar(billingFrame, orient=VERTICAL)
    Treescrollbar.config(command=viewTree.yview)
    Treescrollbar.grid(row=0,column = 1, ipadx=10, sticky='ns')

    #Edit Button
    editbutton = Button(billingButtonFrame, text="Edit", bg="#91cf92", width = int(WR*10), font=('Comic Sans MS',int(FR*12)),command=editOrder)
    editbutton.grid(column=0,row=2,ipadx=8,padx=10, pady = 10)


    #Delete buttons
    deleteItem = Button(billingButtonFrame, text="Delete",cursor ='X_cursor',font=('Comic Sans MS',int(FR*12)),bg="#f54949", width = int(WR*10),command=deleteOrder)
    deleteItem.grid(column=0, row=3, sticky="n",padx=10, pady=10, ipadx=8)


    #Save Bill and complete Transaction
    saveBillButton = Button(billingButtonFrame, text="Save Bill",command=lambda:billingOptions.completeBilling(self,viewTree),
                                    width = int(WR*10),  height = int(HR*2),
                                    font=('Times New Roman', int(FR*15)), bg='#648EF1', fg='#FFFFFF', border=0, cursor = 'hand2')
    saveBillButton.grid(column=0, row=4, sticky="n", padx=10, pady=10, ipadx=8)

    #amountLabel = font.Font(family = 'Helvetica', size = int(FR*22), weight = 'bold')
    #amountTotal = font.Font(family='Helvetica', size=int(FR*22), weight='bold')

    clear_Billing = Button(billingButtonFrame, text="Clear Billing", bg="#f54949",cursor ='X_cursor',
                            width = int(WR*10),  font=('Helvetica', int(FR*12), 'bold'),command=clearBilling)
    clear_Billing.grid(column=0, row=5, sticky="n",padx=10, pady=20, ipadx=8)

    applyDiscountToProduct = Button(billingButtonFrame, text="Apply Discounts", bg='#648EF1', fg='#FFFFFF', cursor='hand2',
                                    width = int(WR*10),  font=('Helvetica', int(FR*12), 'bold'))
    applyDiscountToProduct.grid(column=0, row=6, sticky="n", padx=10, pady=20, ipadx=8)

    #for vatable amount
    VatableAmountLabel = Label(
        amountFrame, width = int(WR*10), text='Vatable        :', bg='#4A2727',font=('Helvetica',int(FR*22),'bold'), fg='#FAF712')
    VatableAmountLabel.grid(row = 1, column = 0,  pady =0, sticky = 'n')

    billingVatableAmountLabel = Label(
        amountFrame, width = int(WR*12), text="", bg="#4A2727",font=('Helvetica',int(FR*22),'bold'), fg='#FAF712')
    billingVatableAmountLabel.grid(row=1, column=1, sticky="n",  pady=0)
    # billingVatableAmountLabel.config(text=billingTotalAmount)

    #total amount
    totalAmountLabel = Label(
        amountFrame, width = int(WR*10), text='Grand Total :',font=('Helvetica',int(FR*22),'bold'), bg='#4A2727', fg='#FAF712')
    totalAmountLabel.grid(row = 2, column = 0,  pady =2, sticky = 'n')

    billingAmountLabel = Label(
        amountFrame, width = int(WR*12), text="", bg="#4A2727", font=('Helvetica',int(FR*22),'bold'), fg='#FAF712')
    billingAmountLabel.grid(row=2, column=1, sticky="n",  pady=2)
    # billingAmountLabel.config(text=billingTotalAmount)

    #print receipt
    # printreceipt= Button(billingFrame,text="Print Receipt",bg="#7ee081",width=10)
    # printreceipt.grid(row=9,column=4,pady=10,ipadx=20)
    