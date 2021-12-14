from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkinter import filedialog
import subprocess

def backupAndRecovery(self):
    try:
        self.displayFrame.destroy()
    except:pass
    self.displayFrame = Frame(self.inventory, bg='#FFFFFF')
    self.displayFrame.pack(fill = "both", side = "left")

    #Function to backup Database
    def backupDatabase():
        nw=datetime.now()
        date = nw.strftime("%d-%m-%Y")
        time = nw.strftime("%H-%M")

        validate = messagebox.askyesno('Backup Request', "Do you want to initiate backup process?")
        if (validate):
            top = Toplevel()
            top.grab_set()
            lbl = Label(top, text = " Backing up Database. Do not close the program ")
            lbl.pack()
            top.geometry("+%d+%d" % (400, 300))

            # Backs up in D drive by default
            command = 'mongodump --db saiRecords --host localhost:27017 --out E:/databaseBackupSI/'+str(date)+'_'+str(time)
            subprocess.call(command,shell=True)
            # os.system(command)
            top.destroy()
            messagebox.showinfo("Request Completed","Database Backup created Successfully")
    #Function to Restore database
    def restoreDatabase():
        filename =  filedialog.askdirectory(initialdir = '/d',
        title = "Select backup File")
        command = "mongorestore --db saiRecords --dir " + str(filename)
        subprocess.call(command,shell=True)
        # os.system(command)
        messagebox.showinfo("Restore Complete","Database Restored Successfully")



    backup_btn = ttk.Button(self.displayFrame, text= 'Back-up Database', command=backupDatabase)
    backup_btn.pack(padx = 50,pady=20, anchor = 'e')
    tips = Label (self.displayFrame, text = '(Use this option to back-up database)')
    tips.pack(padx = 20)

    backup_btn = ttk.Button(self.displayFrame, text='Recover Database', command=restoreDatabase)
    backup_btn.pack(padx=50, pady=20, anchor='e')
    tips = Label(self.displayFrame,
    text='(Use this option to recover database)')
    tips.pack(padx=20)
