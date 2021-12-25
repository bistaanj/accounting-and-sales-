from tkinter import messagebox, ttk
from tkinter import *
import pymongo
from config.dynamicSize import FR, WR, HR
import Frames.Billing.viewProductsInBill as viewProductsInBill
import Frames.Billing.stockManager as sm

# Clears the billing


def clearBilling(self, viewTree):
    try:
        if (self.productsInBill == {}):
            raise ValueError
        validate = messagebox.askokcancel(
            "Billing on Process", "Do you want to Clear Billing ? ")
        if (validate):
            self.productsInBill = {}
            self.billingTotalAmount = 0
            self.billingAmountLabel.config(text=0)
            self.billingVatableAmountLabel.config(text=0)
            viewProductsInBill.viewProductsInBill(self, viewTree)
    except ValueError:
        messagebox.showinfo("Invalid Request",
                            "Billing process not initited yet.")

    # Saves Bill to database


def completeBilling(self, viewTree):
    # Assigns customer's name to the bill and saves to dbs
    def saveBilltoDbs(event=''):
        try:
            if ((askEntry.get()) == ""):
                raise ValueError

            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database('saiRecords')
            # collection = db.inventory

            # For Local Storage
            connection = pymongo.MongoClient("localhost", 27017)
            database = connection['saiRecords']
            collection = database['inventory']
            for product in self.productsInBill:

                print()
                orgValue = int((collection.find_one(
                    {'Product Name': product}))['Quantity'])
                orgValue_sold = int(
                    (collection.find_one({'Product Name': product}))['Sold'])
                orgValue_order = int(
                    (collection.find_one({'Product Name': product}))['Order'])
                newValue = orgValue - \
                    int(self.productsInBill[product]['Quantity'])
                print(newValue)
                collection.find_one_and_update({'Product Name': product},
                                               {'$set': {
                                                   'Quantity': (orgValue-int(self.productsInBill[product]['Quantity'])),
                                               }})

                para1 = self.productsInBill[product]['iid']
                qnty = int(self.productsInBill[product]['Quantity'])
                sm.manageStock(para1, qnty)

                if self.billing_method == 0:
                    collection = database['inventory']
                    collection.find_one_and_update({'Product Name': product},
                                                   {'$set': {
                                                       'Sold': (orgValue_sold+int(self.productsInBill[product]['Quantity'])),
                                                   }})
                else:
                    collection = database['inventory']
                    collection.find_one_and_update({'Product Name': product},
                                                   {'$set': {
                                                       'Order': (orgValue_order+int(self.productsInBill[product]['Quantity'])),
                                                   }})
            dateTime = self.getDateTime()
            billDict = {}
            billDict['Date'] = dateTime[0]
            billDict['Time'] = dateTime[1]
            billDict['Customer Name'] = askEntry.get()
            billDict['Contact Number'] = phnNumEntry.get()
            # Processing the products in bill '.' -> '?'
            new_dict = {}
            a = self.productsInBill
            print(type(new_dict))
            for items in a:
                if '.' in items:
                    processed_string = items.replace('.', '?')
                    new_dict[processed_string] = a[items]
                else:
                    new_dict[items] = a[items]
            print(self.productsInBill)
            billDict['Products'] = {}
            billDict['Products'] = new_dict
            if self.billing_method == 0:
                billDict['Vatable'] = int(self.billingTotalAmount)
                billDict['Grand Total'] = int(
                    int(self.billingTotalAmount)+0.13*int(self.billingTotalAmount))
                collection = database['sales']
                print("bill saved to vat bill")
            else:
                billDict['Grand Total'] = int(self.billingTotalAmount)
                collection = database['order']
                print("bill saved to order data set")
            # collection = db.sales

            collection.insert_one(billDict)
            # Logic to Add value to daily Sales
            # collection = db.dailySalesData
            collection = database['dailySalesData']
            dte = dateTime[0]
            newValue = self.billingTotalAmount
            if (collection.count_documents({'_id': dte}) > 0):
                collection.find_one_and_update(
                    {'_id': dte}, {'$inc': {'daySales': newValue}})
            else:
                collection.insert_one(
                    {'_id': dte, 'daySales': self.billingTotalAmount})
            top.destroy()
            self.productsInBill = {}
            self.billingTotalAmount = 0
            self.billingAmountLabel.config(text=0)
            if self.billing_method == 0:
                self.billingVatableAmountLabel.config(text=0)
            # connection.close()
            viewProductsInBill.viewProductsInBill(self, viewTree)
            messagebox.showinfo('Transaction Completed',
                                'Bill saved to Database')
        except ValueError:
            messagebox.showerror("Insuccifient Data", "Provide Customer Name")

    if (len(self.productsInBill) < 1):
        messagebox.showerror("error", "No Products in Bill ! ")
    else:
        proceedBilling = messagebox.askokcancel(
            "Conformation Required", "Conform Billing ?")
        if(proceedBilling == 1):

            def validateContact(e):
                try:
                    value = int(phnNumEntry.get())
                except ValueError:
                    phnNumEntry.delete(-1, 'end')

            top = Toplevel()
            top.grab_set()
            top.iconbitmap('./res/dsk.ico')
            top.title("Enter Name")
            top.geometry("+%d+%d" % (500, 500))
            askLable = Label(top, text='Customer Name : ',
                             font=('Helvetica', int(FR*15), 'bold'))
            askLable.grid(row=0, column=0, padx=5, pady=5)

            askEntry = Entry(top, width=int(WR*30),
                             font=('Comic Sans MS', int(FR*15), 'bold'))
            askEntry.grid(row=0, column=1, padx=5, pady=5)
            askEntry.bind('<Return>', saveBilltoDbs)
            askEntry.focus_set()
            phnNum = Label(top, text='Contact Number : ',
                           font=('Helvetica', int(FR*15), 'bold'))
            phnNum.grid(row=1, column=0, padx=5, pady=5)
            phnNumEntry = Entry(top, width=int(
                WR*30), font=('Comic Sans MS', int(FR*15), 'bold'))
            phnNumEntry.grid(row=1, column=1, padx=5, pady=5)
            phnNumEntry.bind('<KeyRelease>', validateContact)
            btn = Button(top, text="Enter", width=int(
                WR*10), command=saveBilltoDbs)
            btn.grid(row=2, column=1, padx=5, pady=5)

    # Bill Product's Quantity Edit Function


def applyDiscountProcess(self, viewTree):

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
                viewTree.set(iidEdit, column='Total', value=discount_value)
                new_sales_price = discount_value/orgValue
                self.productsInBill[productname]['Sales Price'] = new_sales_price
                viewTree.set(iidEdit, column='Sales Price',
                             value=new_sales_price)
                self.billingAmountLabel.config(text=self.billingTotalAmount)
            else:
                self.productsInBill[productname]['Sales Price'] = discount_value
                newTotal = discount_value * \
                    float(self.productsInBill[productname]['Quantity'])
                self.productsInBill[productname]['Product Total'] = newTotal
                self.billingTotalAmount += newTotal
                viewTree.set(iidEdit, column='Sales Price',
                             value=discount_value)
                viewTree.set(iidEdit, column='Total', value=newTotal)
                self.billingAmountLabel.config(text=self.billingTotalAmount)

            if self.billing_method == 0:
                self.billingVatableAmountLabel.config(
                    text=int(self.billingTotalAmount))
                self.billingAmountLabel.config(
                    text=int(self.billingTotalAmount+0.13*self.billingTotalAmount))
            top.destroy()
            messagebox.showinfo("Transaction Complete", "Discount Applied")

            # viewTree.set(iidEdit, column='Quantity', value=newValue)

        except ValueError:
            messagebox.showerror("Invalid Request", "Enter new value")

    iidEdit = viewTree.focus()

    if (iidEdit == ""):
        messagebox.showwarning("Warning", "Product Selection Required")
    else:
        top = Toplevel()
        top.grab_set()
        top.iconbitmap('./res/dsk.ico')
        top.geometry("+%d+%d" % (300, 300))
        discountSchemeLabel = Label(
            top, text="Discount Scheme", font=('Helvetica', int(FR*15), 'bold'))
        discountSchemeLabel.grid(row=0, column=0, padx=5, pady=10,)

        schemeType = ttk.Combobox(top, width=int(
            WR*15), values=['Sales Price', 'Product Total'], font=('Comic Sans MS', int(FR*15), 'bold'))
        schemeType.grid(row=0, column=1, padx=5, pady=10,)
        schemeType.current(0)

        quantityLabel = Label(top, text="Enter New Value",
                              font=('Helvetica', int(FR*15), 'bold'))
        quantityLabel.grid(row=2, column=0, padx=5, pady=10,)

        discountedValue = Entry(top, width=int(
            WR*15),  font=('Comic Sans MS', int(FR*15), 'bold'))
        discountedValue.grid(row=2, column=1, padx=5, pady=10,)
        discountedValue.bind('<Return>', applyDiscounts)

        editbtn = Button(top, text="Apply Discount", command=applyDiscounts, font=(
            'Georgia', int(FR*15), 'bold'))
        editbtn.grid(row=3, column=0, pady=10)

    # Removes the product from the Billing Tab's Billing View Tree Table


def removeSelectedRow(self, viewTree):
    try:
        toDelete = viewTree.focus()
        toAddUpValues = viewTree.item(toDelete, 'values')
        productName = toAddUpValues[0]
        productTotal = toAddUpValues[4]
        del self.productsInBill[productName]
        self.billingTotalAmount -= float(productTotal)
        viewProductsInBill.viewProductsInBill(self, viewTree)
        self.billingAmountLabel.config(text=self.billingTotalAmount)
        # self.productTotalLabel.config(text=self.billingTotalAmount)
        if self.billing_method == 0:
            self.billingVatableAmountLabel.config(
                text=int(self.billingTotalAmount))
            self.billingAmountLabel.config(
                text=int(self.billingTotalAmount+0.13*self.billingTotalAmount))
    except IndexError:
        self.warnUser("Product Selection Required")
