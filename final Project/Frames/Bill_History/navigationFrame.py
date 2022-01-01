from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from bson.objectid import ObjectId
from reportlab.pdfgen import canvas
import webbrowser as wb
from config.dynamicSize import FR,WR,HR
from Frames.supportingFunctions import getConnect

def navigationFrame(self, tab):
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

    self.searchhelpFrame = Frame(self.searchLabelFrame)
    self.searchhelpFrame.pack( side = 'left', pady = 10)
    #GUI of view tab

    self.listboxFrame = Frame (self.billdisplayFrame)
    self.listboxFrame.pack(pady = 10, padx = 5)

    self.labelsearchby = Label(self.searchhelpFrame, text="Search By", font=('Comic Sans MS', int(FR*15), 'bold'))
    self.labelsearchby.grid(padx = 5)
    self.helpLabel = Label(self.searchLabelFrame, text='(Set Search filter)', font =('Comic Snas MS', int(FR*12) ))
    self.helpLabel.pack(side='bottom')

    def printBill():
        try:
            billIndex = self.itemlistbox_view.index(ANCHOR)
            billId = self.view_productId[billIndex]

            ##For Cloud Atlas
            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database(self.activeDatabase)
            # collection = db.sales

            ##For Local Database Storage

            collection = getConnect(self.activeDatabase,'sales')
            data = collection.find_one({'_id': ObjectId(billId)})
            # connection.close()
            count = 0
            for rows in view_viewTree.get_children():
                view_viewTree.delete(rows)

            self.dateLabel.config(text= data['Date'])
            self.customerNameLabel.config(text=data['Customer Name'])
            self.timeLabel.config(text=data['Time'])
            self.billTotalLabel.config(text=data['Grand Total'])

            for vlue in (data['Products']):
                if "?" in vlue:
                    processed_name=vlue.replace('?','.')
                else:
                    processed_name=vlue
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
            self.helloat.config(text=data['Contact Number'])
        except (AttributeError, IndexError):
            messagebox.showerror('Invalid Request', 'Bill Selection Required')
        except KeyError:
            self.helloat.config(text='N/A')


    def setSearchTips(event):
        key = self.viewcombobox_search.get()
        if (key == 'Date'):
            self.helpLabel.config(text='(Search Format: DD/MM/YYYY)')
        else:
            self.helpLabel.config(text='(Search Format: Name)')

    
    def displayBillSearch(event=''):
        example = []
        self.view_productId = []
        searchValue = self.billSearchEntry.get()
        key = self.viewcombobox_search.get()
        try:
            self.itemlistbox_view.delete(0, END)
            if (key == ""):
                raise ValueError
            else:
                if (key == 'Date'):
                    searchFilter = '/123/'
                    self.helpLabel.config(text = "(Search Format : DD/MM/YYYY)")
                else:
                    searchFilter = 'i'
                    self.helpLabel.config(text='(Search Format : Name)')
                #For Local database Storage
                collection = getConnect(self.activeDatabase,'sales')

                ##For Cloud Atlas
                # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
                # db = client.get_database(self.activeDatabase)
                # collection = db.sales

                result = collection.find({key: {'$regex': searchValue, '$options': searchFilter}})
                # connection.close()
                for x in result:
                    example.append(x['Customer Name'] + ' ------  ' + x['Date'] + '------' +  x['Contact Number'])
                    self.view_productId.append(x['_id'])

                self.itemlistbox_view.insert(0, *example)
                # if (len(self.view_productId) < 1):
                #     messagebox.showinfo("Search Request", "No Record Found")

        except ValueError:
            messagebox.showerror("Invalid Request", "Set Search Filter")


    self.viewcombobox_search = ttk.Combobox(self.searchLabelFrame, textvariable=4, width = int(WR*12), font = ('Comic Sans MS', int(FR*15)), state = 'readonly')
    self.viewcombobox_search['values'] = (
        'Date',
        'Customer Name',
    )
    self.viewcombobox_search.current(0)


    self.viewcombobox_search.pack(side='left', padx=5)
    self.viewcombobox_search.bind('<<ComboboxSelected>>',setSearchTips)

    #for search bar
    self.billSearchEntry = Entry(self.searchLabelFrame, width = int(WR*38), font =('Comic Snas MS', int(FR*20) ))
    self.billSearchEntry.pack(side='left')
    self.billSearchEntry.bind('<KeyRelease>',displayBillSearch)


    #search button button
    # viewSearch_btn = Button(self.searchLabelFrame, text="Search",
    #                         width = int(WR*10), bg="#6aeb7b", command=displayBillSearch)
    # viewSearch_btn.pack(side='left')


    #for listbox
    self.itemlistbox_view = Listbox(self.listboxFrame, width = int(WR*60), height = int(HR*4), bg="#e8eddf", font =('Comic Snas MS', int(FR*15) ))
    self.itemlistbox_view.grid(column=0, row=0, columnspan=1)


    #for scroll bar
    self.viewScrollbar = Scrollbar(self.listboxFrame, orient=VERTICAL)
    self.viewScrollbar.config(command=self.itemlistbox_view.yview)
    self.viewScrollbar.grid(row=0, ipadx=5, column=5, sticky='ns')

    self.informationFrame = Frame(self.billdisplayFrame)
    self.informationFrame.pack(pady = 5)
    #bill details label

    self.lbl = Label(self.informationFrame, text = "Bill Details", font = ('Comic Snas MS ', int(FR*15), 'bold', 'underline'))
    self.lbl.grid(row = 0, column = 0, columnspan = 4)
    #date label
    self.Viewdatelabel = Label(self.informationFrame, text='Date : ', font = ('Helvetica', int(FR*12)))
    self.Viewdatelabel.grid(row=1, column=0)

    self.dateLabel = Label(self.informationFrame, text='--/--/----', font=('Comic Sans MS', int(FR*15), 'bold'))
    self.dateLabel.grid(row=1, column=1)

    #custumer name label
    self.Viewcustumername = Label(self.informationFrame, text='Customer Name: ', font=('Hevetica', int(FR*12)))
    self.Viewcustumername.grid(row=1, column=2)

    self.customerNameLabel = Label(self.informationFrame, text='---------', font=('Comic Sans MS', int(FR*12), 'bold'))
    self.customerNameLabel.grid(row=1, column=3)

    self.ViewTime = Label(self.informationFrame, text='Time:', font=('Hevetica', int(FR*12)))
    self.ViewTime.grid(row=2, column=0)

    self.timeLabel = Label(self.informationFrame, text='--:-- --',font=('Comic Snas MS', int(FR*12), 'bold'))
    self.timeLabel.grid(row=2, column=1, padx = 10)

    self.helloatLabel = Label(self.informationFrame, text = 'Contact Number', font=('Hevetica', int(FR*12)))
    self.helloatLabel.grid(row = 1, column = 4)

    self.helloat = Label (self.informationFrame, text = ' ----------- ', font = ('Comic Sans MS', int(FR*10), 'bold'))
    self.helloat.grid(row= 1, column=5)

    #Bill Total Labels
    self.billTotal = Label(self.informationFrame, text='Bill Total ', font = ('Helvetica',int(FR*15),'bold'))
    self.billTotal.grid(row=2, column=2,padx = 20)

    self.billTotalLabel = Label(self.informationFrame, text='------ /-', bg='#F2F81D', fg='#164ECF', font=('Helvetica', int(FR*15), 'bold'))
    self.billTotalLabel.grid(row = 2, column = 3)

    self.billFrame = Frame(self.billdisplayFrame)
    self.billFrame.pack()

    view_viewTree = ttk.Treeview(self.billFrame,height = int(HR*10), style="mystyle.Treeview")

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
    Treescrollbar = Scrollbar(self.billFrame, orient=VERTICAL)
    Treescrollbar.config(command=view_viewTree.yview )
    Treescrollbar.pack(side='left' , fill= 'y')

    def searchSale():
        pass

    def customerCopy():
        billIndex = self.itemlistbox_view.index(ANCHOR)
        billId = self.view_productId[billIndex]

        ##For Local Database Storage
        collection = getConnect(self.activeDatabase,'sales')

        ##For Cloud Atlas
        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database(self.activeDatabase)
        # collection = db.sales

        data = collection.find_one({'_id': ObjectId(billId)})

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

    self.dspbill = Button(self.buttonFrame,text="Display Bill", command=printBill, font = ('Helvetica', int(FR*15),'bold'))
    self.dspbill.pack(side="top",pady = 10)

    self.prntBill = Button(self.buttonFrame, text = "Print Bill", command=customerCopy, width = int(WR*15),font = ('Helvetica', int(FR*15),'bold'))
    self.prntBill.pack(side = "top", pady = 10)




    # sendBill = Button(self.buttonFrame, text = "Send Bill")
    # sendBill.pack(pady= 10 )
