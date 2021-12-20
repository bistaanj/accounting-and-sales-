from tkinter import *
from tkinter import ttk
from datetime import datetime
import tkinter.font as font
from config.dynamicSize import FR,WR,HR
from config.configuration import *
# from Frames.Inventory.navigationFrame import navigationFrameInventory
class Window(Tk):
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

        self.overViewTab = ttk.Frame(tab_control)
        tab_control.add(self.overViewTab, text="Overviiiiiiiiiew")


        #Packs the Created Tabs in the Frame
        tab_control.pack(expand = 1, fill = "both")

        #Creates Frame for Navigation Button
        navigationFrameInventory.navigationFrame(self,self.inventory)

        #Creates Frame for Billing Tab
        navigationFrameBilling.navigationFrame(self,self.billingTab)

        #Creates frame for view Button
        navigationFrameBillHistory.navigationFrame(self,self.viewTab)

        #Creates Frame for Settings Tab
        navigationFrameAppSettings.navigationFrame(self,self.settingsTab)

        #Creates Frame for Customer Details
        navigationFrameCustomerDetails.navigationFrame(self,self.customerTab)

        #Creates Frame for Overview
        navigationFrameOverview.navigationFrame(self,self.overViewTab)

        #Creates an Empty Frame to initialize the self.displayFrame
        self.displayFrame = Frame(self.inventory)
        self.displayFrame.pack(fill = "both", side = "left")

        #Style Section for the widgets
        self.myFont = font.Font(family='Helvetica', size=int(FR*20), weight='bold')

        #Displays Inventory Page Initiallt
        addNewRecord.addNewRecord(self,self.inventory)


    #Gets Date and time from system and initialize self.(date/time)
    def getDateTime(self):
        nw = datetime.now()
        date = nw.strftime("%d/%m/%Y")
        time = nw.strftime("%H:%M")
        return (date,time)

    
