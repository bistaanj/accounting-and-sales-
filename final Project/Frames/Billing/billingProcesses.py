from tkinter import *
from tkinter import messagebox
import Frames.Billing.viewProductsInBill as viewProductsInBill

from config.dynamicSize import FR, WR, HR
from Frames.supportingFunctions import warnUser
import pymongo
# New Add Product Funtion to add products in bill


def billingProcess(self, viewTree):
    try:
        def on_closing():
            top.destroy()
            self.executing = False

        def displayToBillView(event=''):
            if askQuantityEntry.get() == "":
                return
            requiredQuantity = float(askQuantityEntry.get())
            salesPrice = float(askSalesPriceEntry.get())
            top.destroy()

            # messagebox.showerror('Invalid Request', 'Quantity must be a number')

            if (float(productToBill['Quantity']) < requiredQuantity or requiredQuantity < 1):
                warnUser("Invalid Entry. Please Check the Available Quantity")
                billingProcess()
            else:
                # try:
                if (productToBill['Product Name'] in self.productsInBill.keys()):
                    warnUser("Product Already in Bill")
                    top.destroy()
                else:
                    self.productsInBill[productToBill['Product Name']] = {}
                    self.productsInBill[productToBill['Product Name']
                                        ]['Quantity'] = requiredQuantity
                    self.productsInBill[productToBill['Product Name']
                                        ]['iid'] = productToBill['_id']
                    self.productsInBill[productToBill['Product Name']
                                        ]['Sales Price'] = salesPrice
                    self.productsInBill[productToBill['Product Name']
                                        ]['Units'] = productToBill['Units']
                    productTotal = int(
                        self.productsInBill[productToBill["Product Name"]]['Sales Price'])*requiredQuantity
                    self.productsInBill[productToBill['Product Name']
                                        ]['Product Total'] = productTotal
                    viewProductsInBill.viewProductsInBill(self, viewTree)
                    top.destroy()

        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.inventory

        # For local database storage

        def validateSalesPrice(e):
            try:
                float(askSalesPriceEntry.get())
            except ValueError:
                askSalesPriceEntry.delete(-1, 'end')

        connection = pymongo.MongoClient("localhost", 27017)
        database = connection['saiRecords']
        collection = database['inventory']
        toadd = self.itemlistbox.get(ANCHOR)
        print("Selected from itemlistbox" + toadd)

        productToBill = collection.find_one({'Product Name': toadd})

        if (productToBill['Quantity'] == 0):
            raise ValueError

        # connection.close()
        top = Toplevel()
        top.grab_set()
        top.iconbitmap('./res/dsk.ico')
        top.geometry("+%d+%d" % (400, 400))
        availableQuantity = Label(
            top, text="Available Quantity", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
        availableQuantity.grid(row=0, column=0)
        displayAvailableQuantity = Label(top, text=(str(productToBill['Quantity'])+" " + str(
            productToBill['Units'])), padx=5, pady=5, font=('Comic Sans MS', int(FR*15), 'bold'))
        displayAvailableQuantity.grid(row=0, column=1)

        askQuantityLabel = Label(top, text="Enter Quantity", padx=5, pady=5, font=(
            'Helvetica', int(FR*15), 'bold'))
        askQuantityLabel.grid(row=1, column=0)

        askQuantityEntry = Entry(top, width=int(
            WR*10), font=('Comic Sans MS', int(FR*15), 'bold'))
        askQuantityEntry.grid(row=1, column=1)

        askSalesPriceLabel = Label(top, text="Sales Price", padx=5, pady=5, font=(
            'Helvetica', int(FR*15), 'bold'))
        askSalesPriceLabel.grid(row=2, column=0)
        askSalesPriceEntry = Entry(top, width=int(
            WR*10), font=('Comic Sans MS', int(FR*15), 'bold'))
        askSalesPriceEntry.insert(0, productToBill['Sales Price'])
        askSalesPriceEntry.grid(row=2, column=1)
        askSalesPriceEntry.bind("<KeyRelease>", validateSalesPrice)

        askQuantityEntry.focus()
        top.bind('<Return>', displayToBillView)

        okBtn = Button(top, text="Sell", padx=5, pady=10, width=int(
            WR*8), font=('Georgia', int(FR*10), 'bold'), command=displayToBillView)
        okBtn.grid(row=3, column=0, columnspan=2)
        top.protocol("WM_DELETE_WINDOW", on_closing)

    except TypeError:
        warnUser("Product Selection Required")
        self.executing = False
        # top.destroy()
    except ValueError:
        self.executing = False
        messagebox.showerror(
            'Invalid Request', 'The selected product seems Out of Stock. Try adding the product in the inventory')


def getConnect(self):
    # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # db = client.get_database('saiRecords')
    # collection = db.inventory
    connection = pymongo.MongoClient('localhost', 27017)
    database = connection['saiRecords']
    collection = database['inventory']
    return collection


def billingEditProcess(self, viewTree):
    def validateQuantity(e):
        try:
            value = int(quantityEntry.get())
        except ValueError:
            quantityEntry.delete(-1, 'end')

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
                viewProductsInBill.viewProductsInBill(self, viewTree)
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
        collection = getConnect(self)
        rslt = collection.find_one({'Product Name': getProduct}, {
            'Quantity': 1, '_id': 0})
        avalQuantity = float(rslt['Quantity'])
        availableQuantity = Label(
            top, text="Available Quantity", padx=5, pady=5, font=('Helvetica', int(FR*15), 'bold'))
        availableQuantity.grid(row=0, column=0)
        displayAvailableQuantity = Label(
            top, text=avalQuantity, padx=5, pady=5, font=('Comic Sans MS', int(FR*15), 'bold'))
        displayAvailableQuantity.grid(row=0, column=1)

        quantityLabel = Label(top, text="Enter New Quantity", padx=5, pady=5, font=(
            'Helvetica', int(FR*15), 'bold'))
        quantityLabel.grid(row=1, column=0)

        quantityEntry = Entry(top, width=int(
            WR*10),  font=('Comic Sans MS', int(FR*15), 'bold'))
        quantityEntry.grid(row=1, column=1)
        quantityEntry.focus()
        quantityEntry.bind('<KeyRelease>', validateQuantity)
        quantityEntry.bind('<Return>', applyEdits)

        editbtn = Button(top, text="Change", command=applyEdits,
                         font=('Georgia', int(FR*10), 'bold'))
        editbtn.grid(row=2, column=0, pady=12)
