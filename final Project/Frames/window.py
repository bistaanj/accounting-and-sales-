from tkinter import *
from tkinter import ttk
from datetime import datetime
import tkinter.font as font
from config.dynamicSize import FR,WR,HR
from config.configuration import *
from Frames.Inventory.features.addNewProduct import addNewRecord

class Window(Tk):
    def __init__(self):
        super(Window,self).__init__()
        self.executing = False
        self.title("Inventory and sales")
        self.iconbitmap('./res/dsk.ico')
        self.geometry('1366x768+0+0')
        # self.maxsize(w,h)
        self.minsize(1366,768)
        # self.maxsize(850,530)
        self.state('zoomed')

        #sets active database for user
        # self.activeDatabase=name 
        
        #for testing phase only
        self.activeDatabase = 'saiRecords'

        # Creates Notebook
        self.tab_control = ttk.Notebook(self)
        notebookstyle = ttk.Style()
        notebookstyle.configure('TNotebook.Tab',font=('URW Gothic L', int(FR*15), 'bold'), padding=[10, 10])

        #Creates Expense Tab
        self.inventory = Frame(self.tab_control, padx = 5, bg = "white" )
        self.tab_control.add(self.inventory, text ="Inventory")

        #Creates Sales Tab
        self.billingTab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.billingTab, text = "Billing")

        #Create overview Tab
        self.overView = ttk.Frame(self.tab_control)
        self.tab_control.add(self.overView,text="Overview")

        #Creates View Tab
        self.customerDetails = ttk.Frame(self.tab_control)
        self.tab_control.add(self.customerDetails, text = "Customer Details")

        self.settingsTab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.settingsTab, text="App Settings")


        #Packs the Created Tabs in the Frame
        self.tab_control.pack(expand = 1, fill = "both")

        #Creates Frame for Navigation Button
        navigationFrameInventory.navigationFrame(self,self.inventory)

        #Creates Frame for Billing Tab
        navigationFrameBilling.navigationFrame(self,self.billingTab)

        #Creates Frame for Overview Tab
        navigationFrameOverview.navigationFrame(self,self.overView)
        
        #Creates frame for customer Details Button
        navigationFrameCustomerDetails.navigationFrame(self,self.customerDetails)

        #Creates Frame for Settings Tab
        navigationFrameAppSettings.navigationFrame(self,self.settingsTab)

        #Creates an Empty Frame to initialize the self.displayFrame
        self.displayFrame = Frame(self.inventory)
        self.displayFrame.pack(fill = "both", side = "left")

        #Style Section for the widgets
        self.myFont = font.Font(family='Helvetica', size=int(FR*20), weight='bold')

        self.tab_control.select(self.inventory)
            
        addNewRecord(self,self.inventory)

        #Displays Inventory Page Initiallt


    #Gets Date and time from system and initialize self.(date/time)
    def getDateTime(self):
        nw = datetime.now()
        date = nw.strftime("%d/%m/%Y")
        time = nw.strftime("%H:%M")
        return (date,time)

    
