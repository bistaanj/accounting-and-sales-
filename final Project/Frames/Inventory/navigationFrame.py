from tkinter import *
from tkinter import messagebox
from config.dynamicSize import FR, WR, HR
from tkinter import ttk
from Frames.Inventory.features.config import *

def navigationFrame(self, tab):
    buttonBg = "#284F9B"
    self.buttonFrame = Frame(tab, bg=buttonBg)
    self.buttonFrame.pack(fill=Y, side="left")

    self.belowFrame = Frame(tab, bg="#d1eded")
    self.belowFrame.pack(fill=X, side="bottom")

    s_btn = ttk.Style()
    s_btn.configure('TButton', height=int(HR*3), width=int(WR*20), border=0,
                    background=buttonBg, font=("Helvetica", int(FR*14), 'bold'))
    s_btn.map('TButton',
              foreground=[('disabled', 'yellow'),
                          ('pressed', 'red'),
                          ('active', '#5A63F5')],
              background=[('disabled', 'magenta'),
                          ('pressed', '!focus', 'cyan'),
                          ('active', 'green')],
              )

    self.btn_addProduct = ttk.Button(self.buttonFrame, text="Add New Product", style='TButton', command= lambda:addNewProduct.addNewRecord(self,tab))
    self.btn_addProduct.grid(column=0, row=1, pady=10)

    self.btn_update = ttk.Button(
        self.buttonFrame, text="Update Inventory", style='TButton', command=lambda:updateInventory.updateInventory(self))
    self.btn_update.grid(column=0, row=2, pady=5)

    self.btn_viewInventory = ttk.Button(
        self.buttonFrame, text="View Inventory", style='TButton', command=lambda:viewInventory.viewInventory(self,tab))
    self.btn_viewInventory.grid(column=0, row=3, pady=5)

    self.btn_viewInventory = ttk.Button(
        self.buttonFrame, text="View Orders", style='TButton', command=lambda:viewOrders.viewOrders(self))
    self.btn_viewInventory.grid(column=0, row=4, pady=5)

    self.btn_checkoutOrders = ttk.Button(
        self.buttonFrame, text="Checkout Orders", style='TButton', command=lambda:checkoutOrders.checkoutOrders(self))
    self.btn_checkoutOrders.grid(column=0, row=5, pady=5)

    backupBtn = ttk.Button(self.buttonFrame, text="Back-up and Recovery",
                           style='TButton', command=lambda:backupAndRecovery.backupAndRecovery(self))
    backupBtn.grid(column=0, row=6, pady=5)

    backupBtn = ttk.Button(self.buttonFrame, text="Day End", style='TButton', command=lambda:dayEnd.dayEnd(self))
    backupBtn.grid(column=0, row=7, pady=5)

    def endSession():
        ans = messagebox.askyesno(
            "Quit", " Any unsaved billing process will not be Saved. Are you sure ?")
        if (ans):
            self.destroy()

    quitbtn = ttk.Button(self.buttonFrame, text="Quit",
                            style='TButton', command=endSession)
    quitbtn.grid(column=0, row=6, pady=20)

     # creates widget inside Inventory Label Frame. Tab-> Inventory
