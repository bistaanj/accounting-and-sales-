import win32api
from config.dynamicSize import FR, WR, HR
from tkinter import *
from tkinter import ttk,messagebox
import pymongo

def viewOrders(self):
    self.displayFrame.destroy()
    self.displayFrame = Frame(self.inventory)
    self.displayFrame.pack(fill="both")

    topFrame = Frame(self.displayFrame)
    topFrame.pack(side=TOP,fill=BOTH)

    orderDetailsFrame = Frame(self.displayFrame)
    orderDetailsFrame.pack()

    bottomFrame = Frame(self.displayFrame)
    bottomFrame.pack(side=BOTTOM)
    def validateContact(e):
        try:
            int(customerPhoneEntry.get())
            displayOrderSearch()
        except ValueError:
            customerPhoneEntry.delete(-1,'end')
            displayOrderSearch()

    def displayInTreeCustomer(event='',y=[]):
        for rows in viewTree.get_children():
            viewTree.delete(rows)
        count = 0
        for i in y:
            for x in i:
                viewTree.insert(parent='', index=END, iid=(i[x]['iid'],i[x]['Date']), text=(count+1),
                values=(i[x]['Date'],x,
                i[x]['Sales Price'],
                i[x]['Quantity'], i[x]['Units'],
                i[x]['Product Total']))
                count+=1

    def displayInTreeProduct(event = '',final=[]):
        for rows in viewTree.get_children():
            viewTree.delete(rows)
        count = 0
        for x in final:
            viewTree.insert(parent='', index=END, iid=(final[x]), text=(count+1),
                values=(final[x]['date'],final[x]['cName'],
                final[x]['product']['Sales Price'],
                final[x]['product']['Quantity'], final[x]['product']['Units'],
                final[x]['product']['Product Total']))
            count+=1

    def displayFromList(event = ''):
        index = itemlistbox.index(ANCHOR)
        item = itemlistbox.get(index)
        if len(item) > 0:
            connection = pymongo.MongoClient("localhost", 27017)
            database = connection[self.activeDatabase]
            collection = database['order']
            allOrders = collection.find()
            connection.close()
            if PtypeCombo.get() == "By Customer":
                y = []
                for x in allOrders:
                    if x['Contact Number'] in item and x['Customer Name'] in item:
                        raw = {}
                        raw = x['Products']
                        for k in list(raw):
                            raw[k]['Date']=x['Date']
                        y.append(raw)
                displayInTreeCustomer('',y)
            else:
                final = {}
                for i in allOrders:
                    for a in i['Products']:
                        if  a.lower() in item.lower():
                            process1 = {'date':i['Date'],'cName' :i['Customer Name'], 'product': i['Products'][a]}
                            final[i['_id']]=process1
                displayInTreeProduct('',final)
    
    def displayOrderSearch(event=''):
        itemlistbox.delete(0,END)
        key = PtypeCombo.get()
        try:
            if (key == ""):
                raise ValueError
            else:
                #For Local database Storage
                connection = pymongo.MongoClient("localhost", 27017)
                database = connection[self.activeDatabase]
                collection = database['order']
                if(key == 'By Product'):
                    customerNameEntry.grid_forget()
                    customerNameLabel.grid_forget()
                    customerPhoneEntry.grid_forget()
                    customerPhoneLabel.grid_forget()
                    customerName.pack_forget()
                    checkoutAllOrderButton.pack_forget()
                    searchBox.grid(column=2, row=1, padx = 10, pady=10)
                    productNameLabel.grid(column=1,row=1)
                    checkoutAllProductsButton.pack(side=LEFT,padx=20)
                    searchBox.bind('<KeyRelease>', displayOrderSearch)
                    searchBox.bind('<Return>')
                    searchValue = searchBox.get()
                    viewTree.heading('Customer Name', text='Customer Name', anchor=CENTER)

                    temp2= {}
                    temp = collection.find()
                    for i in temp:
                        for k in i['Products']:
                            if len(searchValue)>0:
                                if searchValue.lower() in k.lower():
                                    try:
                                        temp2[k] = temp2[k]+i['Products'][k]['Quantity']
                                    except:
                                        temp2[k] = i['Products'][k]['Quantity']
                            else:
                                try:
                                    temp2[k] = temp2[k]+i['Products'][k]['Quantity']
                                except:
                                    temp2[k] = i['Products'][k]['Quantity']
                    j=0

                    for i in temp2:
                        i.replace("?",".")
                        itemlistbox.insert(j,i+' --- '+str(temp2[i]))
                        j+=1
                    final = {}
                    result= collection.find({})
                    process1 = {}
                    final={}
                    if '.' in searchValue:
                        searchValue = searchValue.replace('.','?')

                    for i in result:
                        for a in i['Products']:
                            if searchValue.lower() == a.lower():
                                # print(searchValue)
                                process1 = {'date':i['Date'],'cName' :i['Customer Name'], 'product': i['Products'][a]}
                                final[i['_id']]=process1
                    displayInTreeProduct('',final)
                    
                else:
                    contact = customerPhoneEntry.get()
                    allOrders = collection.find()
                    connection.close()
                    y=[]
                    self.nameAndPhoneNumber = {}
                    for x in allOrders:
                        if len(contact) > 0:
                            if x['Contact Number'] == contact:
                                self.nameAndPhoneNumber[x['_id']] = x['Customer Name'] +' --- ' + x['Contact Number']
                                raw = {}
                                raw = x['Products']
                                for k in list(raw):
                                    raw[k]['Date']=x['Date']
                                y.append(raw)
                        else:
                            self.nameAndPhoneNumber[x['_id']] = x['Customer Name'] +' --- ' + x['Contact Number']

                    displayInTreeCustomer('',y)
                    itemlistbox.insert(0,*self.nameAndPhoneNumber.values())
                    
                    customerNameLabel.grid(column =1,row =1,pady=5,padx=15)
                    customerNameEntry.grid(column=2,row=1,pady=5,padx=15)
                    customerPhoneLabel.grid(column =1,row =2,pady=5,padx=15)
                    customerPhoneEntry.grid(column=2,row=2,pady=5,padx=15)
                    checkoutAllOrderButton.pack(side=LEFT)
                    customerPhoneEntry.bind('<KeyRelease>',validateContact)
                    searchBox.grid_forget()
                    productNameLabel.grid_forget()
                    checkoutAllProductsButton.pack_forget()
                    viewTree.heading('Customer Name', text='Product Name', anchor=CENTER)
                    
        except ValueError:
            messagebox.showerror("Invalid Request", "Set Search Filter")


    PtypeCombo = ttk.Combobox(topFrame, background='#CED7D7',width = int(WR*10), values=['By Customer', 'By Product'],font=('Comic Sans MS',int(FR*10),'bold'),state = 'readonly')
    PtypeCombo.current(0)
    PtypeCombo.grid(column = 0, row = 0, padx = 15, pady = 10, sticky = "w")
    PtypeCombo.bind('<<ComboboxSelected>>', displayOrderSearch)
    productNameLabel = Label(topFrame,text="Product Name:",font=('Comic Sans MS', int(FR*12)))
    productNameLabel.grid_forget()
    searchBox = Entry(topFrame, font=('Hevitica', int(FR*13),'bold'), width=int(WR*20))
    searchBox.grid_forget()

    customerNameLabel = Label(topFrame,text="Customer Name: ", font=('Comic Sans MS', int(FR*12)))
    customerNameLabel.grid(column =1,row =1,pady=5,padx=15)

    customerNameEntry = Entry(topFrame, font=('Hevitica', int(FR*11),'bold'), width= int(WR*20))
    customerNameEntry.grid(column=2,row=1,pady=5,padx=15)

    customerPhoneLabel = Label(topFrame,text="Mobile Number: ", font=('Comic Sans MS', int(FR*12)))
    customerPhoneLabel.grid(column =1,row =2,pady=5,padx=15)

    customerPhoneEntry = Entry(topFrame, font=('Hevitica', int(FR*11),'bold'), width= int(WR*20))
    customerPhoneEntry.grid(column=2,row=2,pady=5,padx=15)
    customerPhoneEntry.bind('<KeyRelease>',validateContact)

    btn_search = Button(topFrame, text='Search', bg = '#3399ff', fg = '#ffffff', border = 0,font=('Comic Sans MS', int(FR*13),'bold'),command=displayOrderSearch)
    btn_search.grid(row=1, column=3, padx = 25, pady = 10,rowspan=2)

    customerName = Label(orderDetailsFrame,text='',font=('Comic Sans MS', int(FR*13)))
    customerName.pack()

    itemlistbox = Listbox(orderDetailsFrame, width = int(WR*20), height = int(HR*3), bg="#e8eddf", font =('Comic Snas MS', int(FR*14) ))
    itemlistbox.pack(side=LEFT,fill=Y,pady=20)
    itemlistbox.bind('<<ListboxSelect>>',displayFromList)

    scrollbar = Scrollbar(orderDetailsFrame, orient=VERTICAL)
    scrollbar.config(command=itemlistbox.yview)
    scrollbar.pack(side=LEFT,fill=Y,pady=20)

    viewTree = ttk.Treeview(orderDetailsFrame,  style="mystyle.Treeview", height=13)

    #Define Columns
    viewTree['columns'] = ('Date','Customer Name',
                            'Sales Price', 'Quantity', 'Units', 'Total Price')
    viewTree.column('#0', width = int(WR*40), minwidth=10, anchor=CENTER)
    viewTree.column('Date',width=int(WR*100),anchor=CENTER)
    viewTree.column('Customer Name', width = int(WR*140), anchor=CENTER)
    viewTree.column('Sales Price', width = int(WR*130), anchor=CENTER)
    viewTree.column('Quantity', width = int(WR*110), anchor=CENTER)
    viewTree.column('Units', width = int(WR*100), anchor=CENTER)
    viewTree.column('Total Price', width = int(WR*140), anchor=CENTER)

    #Create Headings
    viewTree.heading('#0', text='S.N', anchor=CENTER)
    viewTree.heading('Date', text='Date', anchor=CENTER)
    viewTree.heading('Customer Name', text='Product Name', anchor=CENTER)
    viewTree.heading('Sales Price', text='Sales Price', anchor=CENTER)
    viewTree.heading('Quantity', text='Quantity', anchor=CENTER)
    viewTree.heading('Units', text='Units', anchor=CENTER)
    viewTree.heading('Total Price', text='Total Price', anchor=CENTER)
    viewTree.pack(fill = 'both',expand = 1, padx = 20,pady = 20)
    viewTree = viewTree
    
    checkoutSelectedButton = Button(bottomFrame,text="Checkout Selected",bg = '#3399ff', fg = '#ffffff', border = 0,font=('Comic Sans MS', int(FR*13)))
    checkoutSelectedButton.pack(side=LEFT,padx=20)

    checkoutAllProductsButton =Button(bottomFrame,text="Checkout All Product",bg = '#3399ff', fg = '#ffffff', border = 0,font=('Comic Sans MS', int(FR*13)))
    checkoutAllProductsButton.pack_forget()

    checkoutAllOrderButton = Button(bottomFrame,text="Checkout All Order",bg = '#3399ff', fg = '#ffffff', border = 0,font=('Comic Sans MS', int(FR*13)))
    checkoutAllOrderButton.pack_forget()

    
    displayOrderSearch()
