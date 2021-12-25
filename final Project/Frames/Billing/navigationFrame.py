from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import win32api
import pymongo
from config.dynamicSize import FR, WR, HR
from Frames.Billing.config import *
# creates frame and buttons inside the Billing tab's Navigation Button


def navigationFrame(self, tab):
    self.billing_method = 0
    self.billingTotalAmount = 0
    self.productsInBill = {}
    buttonBg = "#284F9B"
    self.buttonFrame = Frame(tab, bg=buttonBg)
    self.buttonFrame.pack(side=LEFT, fill=Y)

    s_btn = ttk.Style()
    s_btn.configure('TButton', height=int(HR*3), width=int(WR*20), border=0,
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

    self.btn_addProduct = ttk.Button(self.buttonFrame, text="VAT Billing",
                                     style='TButton', command=lambda: vat.vat_billing(self, viewTree))
    self.btn_addProduct.grid(column=0, row=1, pady=10)

    self.btn_update = ttk.Button(self.buttonFrame, text="Order",
                                 style='TButton', command=lambda: order.order(self, viewTree))
    self.btn_update.grid(column=0, row=2, pady=5)

    self.displayFrame = Frame(tab, bg="white")
    self.displayFrame.pack(fill='both')

    self.billingtypeFrame = Frame(self.displayFrame, bg='white')
    self.billingtypeFrame.pack(fill='x')

    self.mainBillingFrame = Frame(self.displayFrame, bg='white')
    self.mainBillingFrame.pack(
        side='left', fill='both', padx=20, pady=25, ipady=10)

    self.billingButtonFrame = Frame(self.displayFrame, bg='white')
    self.billingButtonFrame.pack(side='left', fill='both', pady=15, ipady=10)
    # self.billingButtonFrame.grid(column=1, row=0, sticky=NS)

    self.billingSearchFrame = Frame(self.mainBillingFrame, bg='white')
    self.billingSearchFrame.pack(padx=30)
    # self.billingSearchFrame.grid(column = 0, row = 0, pady = 15)

    self.billingFrame = Frame(self.mainBillingFrame, bg='white')
    self.billingFrame.pack(padx=10, pady=10)
    # self.billingFrame.grid(column = 0, row = 1, pady = 15)

    self.amountFrame = Frame(self.mainBillingFrame, bg='white')
    self.amountFrame.pack(pady=10)
    # self.amountFrame.grid(column = 0, row = 2)

    # Displays Product in the Listbox of billing tabs to search for Product
    def displayProductOptions(event=''):
        example = []
        searchValue = self.billingSearchEntry.get()

        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.inventory

        # For local storage
        connection = pymongo.MongoClient("localhost", 27017)
        database = connection['saiRecords']
        collection = database['inventory']
        result = collection.find(
            {"Product Name": {'$regex': searchValue, '$options': 'i'}})
        # connection.close()
        for x in result:
            example.append(x['Product Name'])
        self.itemlistbox.delete(0, END)
        self.itemlistbox.insert(0, *example)

    def callback(event=''):
        if not self.executing and self.tab_control.tab(self.tab_control.select(), "text") == "Billing":
            self.executing = True
            state_left = win32api.GetKeyState(0x01)
            if state_left < 0:
                billingProcess.billingProcess(self, viewTree)

    # Billing GUI starts here

    # for billing name
    self.billtypelabel = Label(self.billingtypeFrame, text="VAT BILLING",
                               bg='#FFFFFF', font=('Helvetica', int(FR*30), 'bold', 'underline'), fg="#5A63F5", border=0)
    self.billtypelabel.pack(fill="both", side="top")

    self.searchlabel = Label(self.billingSearchFrame, text=" Name", font=(
        'Helvetica', int(FR*12), 'bold'), bg='white')
    self.searchlabel.grid(column=0, row=1, padx=15)
    # for search bar
    self.billingSearchEntry = Entry(self.billingSearchFrame, width=int(
        WR*35), font=('Helvetica', int(FR*20), 'bold'), bg='#f7eeee')
    self.billingSearchEntry.grid(column=1, row=1, padx=15)
    self.billingSearchEntry.bind('<KeyRelease>', displayProductOptions)

    # add button button
    self.searchButton = Button(self.billingSearchFrame, text="Add Product", font=('Helvetica', int(
        FR*14), 'bold'), width=int(WR*10), bg="#6aeb7b", command=lambda: billingProcess.billingProcess(self, viewTree))
    self.searchButton.grid(column=5, row=1)

    # for listbox
    self.itemlistbox = Listbox(
        self.billingSearchFrame, width=int(WR*80), height=int(HR*5), bg="#e8eddf")
    self.itemlistbox.grid(column=1, row=2, columnspan=4, pady=0)
    self.itemlistbox.bind("<<ListboxSelect>>", callback)

    # for scroll bar
    self.scrollbar = Scrollbar(self.billingSearchFrame, orient=VERTICAL)
    self.scrollbar.config(command=self.itemlistbox.yview)
    self.scrollbar.grid(row=2, ipadx=10, column=5, sticky='ns')

    # treeview Styling
    vtStyle = ttk.Style()
    vtStyle.configure('Treeview.Heading', font=(
        'Comic Sans MS', int(FR*12), 'bold'))
    treeStyle = ttk.Style()

    treeStyle.configure("mystyle.Treeview", highlightthickness=1,
                        bd=0, rowheight=int(HR*25), font=('Georgia', int(FR*13)))
    # treeStyle.layout('mystyle.Treeview',[('mystyle.Treeview.treearea',{'sticky':'nswe'})])

    # treeview
    viewTree = ttk.Treeview(self.billingFrame, height=int(
        HR*10), style="mystyle.Treeview")
    # Define Columns
    viewTree['columns'] = ('Product Name', 'Quantity',
                           'Units', 'Sales Price', 'Total')
    viewTree.column('#0', width=int(WR*40), minwidth=20, anchor=CENTER)
    viewTree.column('Product Name', width=int(WR*300), anchor='w')
    viewTree.column('Quantity', width=int(WR*130), anchor=CENTER)
    viewTree.column('Units', width=int(WR*60), anchor=CENTER)
    viewTree.column('Sales Price', width=int(WR*130), anchor=CENTER)
    viewTree.column('Total', width=int(WR*130), anchor=CENTER)

    # Create Headings
    viewTree.heading('#0', text='S.N', anchor=CENTER)
    viewTree.heading('Product Name', text='Product Name', anchor=CENTER)
    viewTree.heading('Quantity', text='Quantity', anchor=CENTER)
    viewTree.heading('Units', text='Units', anchor=CENTER)
    viewTree.heading('Sales Price', text='Price per unit', anchor=CENTER)
    viewTree.heading('Total', text='Total', anchor=CENTER)
    viewTree.grid(row=0, column=0,)

    # for scroll bar
    Treescrollbar = Scrollbar(self.billingFrame, orient=VERTICAL)
    Treescrollbar.config(command=viewTree.yview)
    Treescrollbar.grid(row=0, column=1, ipadx=10, sticky='ns')

    # Edit Button
    self.editbutton = Button(self.billingButtonFrame, text="Edit", bg="#91cf92", command=lambda: billingProcess.billingEditProcess(
        self, viewTree), width=int(WR*10), font=('Comic Sans MS', int(FR*12)))
    self.editbutton.grid(column=0, row=2, ipadx=8, padx=10, pady=10)

    # Delete buttons
    self.additem = Button(self.billingButtonFrame, text="Delete", cursor='X_cursor', font=('Comic Sans MS', int(
        FR*12)), bg="#f54949", width=int(WR*10), command=lambda: billingOptions.removeSelectedRow(self, viewTree))
    self.additem.grid(column=0, row=3, sticky="n", padx=10, pady=10, ipadx=8)

    # Save Bill and complete Transaction
    saveBillButton = Button(self.billingButtonFrame, text="Save Bill",
                            width=int(WR*10),  height=int(HR*2), command=lambda: billingOptions.completeBilling(self, viewTree),
                            font=('Times New Roman', int(FR*15)), bg='#648EF1', fg='#FFFFFF', border=0, cursor='hand2')
    saveBillButton.grid(column=0, row=4, sticky="n", padx=10, pady=10, ipadx=8)

    #amountLabel = font.Font(family = 'Helvetica', size = int(FR*22), weight = 'bold')
    #amountTotal = font.Font(family='Helvetica', size=int(FR*22), weight='bold')

    clear_Billing = Button(self.billingButtonFrame, text="Clear Billing", bg="#f54949", cursor='X_cursor',
                           width=int(WR*10),  font=('Helvetica', int(FR*12), 'bold'), command=lambda: billingOptions.clearBilling(self, viewTree))
    clear_Billing.grid(column=0, row=5, sticky="n", padx=10, pady=20, ipadx=8)

    applyDiscountToProduct = Button(self.billingButtonFrame, text="Apply Discounts", bg='#648EF1', fg='#FFFFFF', cursor='hand2',
                                    width=int(WR*10),  font=('Helvetica', int(FR*12), 'bold'), command=lambda: billingOptions.applyDiscountProcess(self, viewTree))
    applyDiscountToProduct.grid(
        column=0, row=6, sticky="n", padx=10, pady=20, ipadx=8)

    # for vatable amount
    self.VatableAmountLabel = Label(
        self.amountFrame, width=int(WR*10), text='Vatable        :', bg='#4A2727', font=('Helvetica', int(FR*22), 'bold'), fg='#FAF712')
    self.VatableAmountLabel.grid(row=1, column=0,  pady=0, sticky='n')

    self.billingVatableAmountLabel = Label(
        self.amountFrame, width=int(WR*12), text="", bg="#4A2727", font=('Helvetica', int(FR*22), 'bold'), fg='#FAF712')
    self.billingVatableAmountLabel.grid(row=1, column=1, sticky="n",  pady=0)
    # self.billingVatableAmountLabel.config(text=self.billingTotalAmount)

    # total amount
    self.totalAmountLabel = Label(
        self.amountFrame, width=int(WR*10), text='Grand Total :', font=('Helvetica', int(FR*22), 'bold'), bg='#4A2727', fg='#FAF712')
    self.totalAmountLabel.grid(row=2, column=0,  pady=2, sticky='n')

    self.billingAmountLabel = Label(
        self.amountFrame, width=int(WR*12), text="", bg="#4A2727", font=('Helvetica', int(FR*22), 'bold'), fg='#FAF712')
    self.billingAmountLabel.grid(row=2, column=1, sticky="n",  pady=2)
    self.billingAmountLabel.config(text=self.billingTotalAmount)

    # print receipt
    # self.printreceipt= Button(self.billingFrame,text="Print Receipt",bg="#7ee081",width=10)
    # self.printreceipt.grid(row=9,column=4,pady=10,ipadx=20)
