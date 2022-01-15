from tkinter import *
from tkinter import ttk
from Frames.App_Settings.mailOptions import mailOptions 
def navigationFrame(self,tab):
    
    self.displayFrame = Frame(tab)
    self.displayFrame.pack(fill="both", padx=20, pady=20)
    
    mailOptions(self,tab)
    # def callback(e=""):
        
    #     def back(e=""):
    #         self.displayFrame.pack_forget()
    #         displayFrame.pack(fill="both", padx=20, pady=20)

    #     displayFrame.pack_forget()
    #     self.displayFrame = Frame(tab)
    #     self.displayFrame.pack(fill="both", padx=20, pady=20)
    #     backButton = Button(self.displayFrame,text="Back",command=back)
    #     backButton.grid(row=8,column=0)
    #     mailOptions(self,tab)
    
    # mailButton = Button(displayFrame,text="Mail Details",command= callback)
    # mailButton.pack()
    