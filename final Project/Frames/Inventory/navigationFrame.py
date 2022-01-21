from tkinter import *
from tkinter import messagebox
from tkinter import font
from config.dynamicSize import FR, WR, HR
from tkinter import ttk
from Frames.Inventory.features.config import *
from authentication import authentication
# import main

def navigationFrame(self, tab):
    buttonBg = "#30353b"
    self.buttonFrame = Frame(tab, bg=buttonBg)
    self.buttonFrame.pack(fill=Y, side="left")

    self.belowFrame = Frame(tab, bg="#d1eded")
    self.belowFrame.pack(fill=X, side="bottom")

    s_btn = ttk.Style()
    s_btn.configure("TButton", bg = '#30353b', border=0)
    # s_btn.map('TButton',
    #           foreground=[('disabled', 'yellow'),
    #                       ('pressed', 'red'),
    #                       ('active', '#white')],
    #           background=[('disabled', 'white'),
    #                       ('pressed', '!focus', '#30353b'),
    #                       ('active', 'green')],
    #           )
    self.btn_addProduct = Button(self.buttonFrame,background='#30353b', cursor='hand2',font=('Helvetical', int(FR*15)), border = 0 ,fg='white',text="Add New Product", command= lambda:addNewProduct.addNewRecord(self,tab))
    self.btn_addProduct.grid(column=0, row=1, pady= int(HR*10))

    self.btn_update = Button(self.buttonFrame, text="Update Inventory",background='#30353b', cursor='hand2',font=('Helvetical', int(FR*15)), border = 0 ,fg='white',command=lambda:updateInventory.updateInventory(self))
    self.btn_update.grid(column=0, row=2, pady=int(HR*10))

    self.btn_viewInventory = Button(self.buttonFrame, text="View Inventory",background='#30353b', cursor='hand2',font=('Helvetical', int(FR*15)), border = 0 ,fg='white', command=lambda:viewInventory.viewInventory(self,tab))
    self.btn_viewInventory.grid(column=0, row=3, pady=int(HR*10))

    self.btn_checkoutOrders = Button(self.buttonFrame, text="Checkout Orders",background='#30353b', cursor='hand2',font=('Helvetical', int(FR*15)), border = 0 ,fg='white', command=lambda:checkoutOrders.checkoutOrders(self))
    self.btn_checkoutOrders.grid(column=0, row=5, pady=int(HR*10))

    backupBtn = Button(self.buttonFrame, text="Back-up and Recovery",
                          background='#30353b', cursor='hand2',font=('Helvetical', int(FR*15)), border = 0 ,fg='white', command=lambda:backupAndRecovery.backupAndRecovery(self))
    backupBtn.grid(column=0, row=6, pady=int(HR*10))

    backupBtn = Button(self.buttonFrame, text="Day End",background='#30353b', cursor='hand2',font=('Helvetical', int(FR*15)), border = 0 ,fg='white', command=lambda:dayEnd.dayEnd(self))
    backupBtn.grid(column=0, row=7, pady=int(HR*10))

   
    def endSession():
        ans = messagebox.askyesno(
            "Logout", " Any unsaved billing process will not be Saved. Are you sure ?")
        if (ans):
            self.destroy()
            authUser = authentication.AuthUser()
            authUser.mainloop()

    quitbtn = Button(self.buttonFrame, text="Logout", background='#30353b', cursor='hand2',font=('Helvetical', int(FR*15)), border = 0 ,fg='white', command=endSession)
    quitbtn.grid(column=0, row=8, pady=20)

     # creates widget inside Inventory Label Frame. Tab-> Inventory
