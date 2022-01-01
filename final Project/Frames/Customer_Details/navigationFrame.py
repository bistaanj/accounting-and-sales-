from tkinter import ttk
from tkinter import *
from config.dynamicSize import FR,WR,HR,nepaliDate
from pyBSDate import convert_AD_to_BS
from datetime import datetime
from Frames.supportingFunctions import getConnect

def navigationFrame(self, tab):
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
            if 'Sales' in self.name_list[index]:
                Collection=  getConnect(self.activeDatabase,'sales')
            else:
                Collection= getConnect(self.activeDatabase,'order')
            bill=Collection.find_one({'_id':self.billpointer[index]})
            
            if nepaliDate:
                addDate = datetime.date(datetime.strptime(bill['Date'],"%d/%m/%Y"))
                bsdate = convert_AD_to_BS(addDate.year,addDate.month,addDate.day)
                dateLabel.config(text=str(bsdate[0])+"-"+str(bsdate[1])+"-"+str(bsdate[1]))
            else:
                dateLabel.config(text=bill['Date'])
            timeLabel.config(text=bill['Time'])
            customerNameLabel.config(text=bill['Customer Name'])
            helloat.config(text=bill['Contact Number'])
            billTotalLabel.config(text=bill['Grand Total'])

            count=0
            for rows in view_viewTree.get_children():
                view_viewTree.delete(rows)


            for vlue in (bill['Products']):
                if "?" in vlue:
                    processed_name=vlue.replace('?','.')
                else:
                    processed_name=vlue
                    view_viewTree.insert(parent='', index=END,
                                        iid=(bill['Products'][vlue]['iid']), text=(count+1), values=( processed_name ,
                                        bill['Products'][vlue]['Quantity'],
                                        bill['Products'][vlue]['Sales Price'],
                                        bill['Products'][vlue]['Product Total']))

        def searchCustomer():
            name = ent_name.get()
            number = ent_phone.get()
            collection = getConnect(self.activeDatabase,'sales')
            billList.delete(0, END)

            self.name_list = []
            self.billpointer= []
            totalPurchase = 0
            result = collection.find({'Customer Name':{'$regex': name, '$options': 'i' } , 'Contact Number': number})

            for x in result:
                    totalPurchase+=x['Grand Total']
                    self.name_list.append(
                        x['Customer Name'] +  '------' + x['Date'] + '---' + 'Sales')
                    self.billpointer.append(x['_id'])
                    # self.view_productId.append(x['_id'])
            collection = getConnect(self.activeDatabase,'order')
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
