from tkinter import *
from tkinter import messagebox,ttk
import pymongo
from config.dynamicSize import FR,WR,HR

def navigationFrame(self,tab):
    
    self.displayFrame = Frame(tab)
    self.displayFrame.pack(fill="both", padx=20, pady=20)

    def configureSettingsData(key,value):
        self.UpdatePopUp.destroy()

        ##For local Database storage
        connection = pymongo.MongoClient('localhost',27017)
        dbs = connection['saiRecords']
        collection = dbs['configuration']

        ##For Cloud Atlas
        # client = MongoClient(
        #     "mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.configuration


        collection.find_one_and_update({'_id': 'settingsData'},{'$set':{key:value}})
        data = collection.find_one({'_id':'settingsData'})
        self.sender_emaildata.config(text = data['sender_email'])
        self.receiver_emaildata.config(text = data['receiver_email'])
        self.master_passworddata.config(text=data['master_password'])
        self.sender_passworddata.config(text=data['sender_password'])

        messagebox.showinfo('Value Updated','Value has been successfully Updated')


    # Functions to Update Values in the Database
    def update_sender():
        value = self.AppsSettingsEntry.get()
        configureSettingsData('sender_email', value)

    def update_receiver():
        value = self.AppsSettingsEntry.get()
        configureSettingsData('receiver_email', value)

    def update_senderPassword():
        value = self.AppsSettingsEntry.get()
        configureSettingsData('sender_password', value)
    def update_MasterPassword():
        value = self.AppsSettingsEntry.get()
        print('Flag3')
        configureSettingsData('master_password', value)

    #Displays pop-Up to get new Values
    def displayTop(displayText,cmd):
        self.UpdatePopUp = Toplevel()
        self.UpdatePopUp.grab_set()
        self.UpdatePopUp.title("Update Values")

        self.UpdatePopUp.geometry("+%d+%d" % (400, 300))
        # self.UpdatePopUp.minsize(200,200)

        updateLabel = Label(self.UpdatePopUp, text=displayText)
        updateLabel.grid(row = 0, column = 0,padx=10, pady=10)
        self.AppsSettingsEntry = Entry(self.UpdatePopUp, width=20)
        self.AppsSettingsEntry.grid(row = 1, column = 0,padx=10, pady=10)
        self.AppsSettingsEntry.focus()
        print("Flag1")
        updateBtn = Button(self.UpdatePopUp, text="Update Value", command=cmd)
        updateBtn.grid(row=2, column=0, padx=10, pady=20)



    # # Functions to Display pop up and get new values
    def getNewSender():
        displayTop('Enter New Sender Mmail-id',update_sender)

    def getNewSenderPassword():
        displayTop('Enter New Sender Password', update_senderPassword)

    def getNewReceiver():
        displayTop('Enter New Receiver Mail-id', update_receiver)

    def getMasterPassword():
        print('Flag2')
        displayTop('Enter New Master Password', update_MasterPassword)

    #Displays content in the App Settings Tab after authentyication
    def displayContents():
        try:

            ##For local database storage
            connection = pymongo.MongoClient('localhost',27017)
            dbs = connection['saiRecords']
            collection = dbs['configuration']

            #For Cloud Atlas
            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database('saiRecords')
            # collection = db.configuration

            sysData=collection.find_one({'_id': 'settingsData'})
            print(sysData)
            connection.close()
            receiverLabel = Label(self.displayFrame, text = " Send mail using :", font = ('Helvetica', int(FR*10),'bold'))
            receiverLabel.grid(row=0, column=0, padx=10, pady=10, sticky='w')

            infoLabel = Label(self.displayFrame, text=" (Set this email address send backup)")
            infoLabel.grid(row=1, column=0, columnspan=2,padx=10, pady=0, sticky='w')

            self.sender_emaildata = Label(self.displayFrame, text=sysData['sender_email'], font=('Helvetica', int(FR*10), 'bold'))
            self.sender_emaildata.grid(row = 0, column = 1, padx = 10, pady = 10)

            senderPasswordLabel = Label(self.displayFrame, text = " Sender email password :",font = ('Helvetica', int(FR*10),'bold'))
            senderPasswordLabel.grid(
                row=2, column=0, padx=10, pady=10, sticky='w')

            infoLabel = Label(self.displayFrame, text=" (Password of the sender's email address)")
            infoLabel.grid(row=3, column=0, columnspan=2,
                        padx=10, pady=0, sticky='w')

            self.sender_passworddata = Label(self.displayFrame, text='*********', font=('Helvetica', int(FR*10), 'bold'))#sysData['sender_password']
            self.sender_passworddata.grid(row=2, column=1, padx=10, pady=10)

            receiverLabel = Label(self.displayFrame, text= " Receive mail in: ", font = ('Helvetica', int(FR*10), 'bold'))
            receiverLabel.grid(row=4, column=0, padx=10, pady=10, sticky='w')

            infoLabel = Label(self.displayFrame, text=" (Set this email address to receive backup)")
            infoLabel.grid(row = 5, column = 0,columnspan = 2, padx = 10, pady = 0, sticky='w')

            self.receiver_emaildata = Label(self.displayFrame, text = sysData['sender_email'],font = ('Helvetica', int(FR*10),'bold'))
            self.receiver_emaildata.grid(row = 4, column = 1, padx = 10, pady = 10)

            masterPasswordLabel = Label(self.displayFrame, text = "Master Password :",font = ('Helvetica', int(FR*10),'bold'))
            masterPasswordLabel.grid(
                row=6, column=0, padx=10, pady=10, sticky='w')

            infoLabel = Label(self.displayFrame,text=" (Password to access the Setting Tab)")
            infoLabel.grid(row=7, column=0, columnspan=2,
                        padx=10, pady=0, sticky='w')

            self.master_passworddata = Label(self.displayFrame, text=sysData['master_password'], font=('Helvetica', int(FR*10), 'bold'))
            self.master_passworddata.grid(row = 6, column = 1, padx = 10, pady = 10)

            upd_btn=ttk.Style()
            upd_btn.configure('Update.TButton',width = int(WR*10), font=('Times New Roman',int(FR*10)))

            upd_sendermail = ttk.Button(self.displayFrame, text ="Update", style = 'Update.TButton', command =getNewSender)
            upd_sendermail.grid(row =0 , column =2 )

            upd_mailPassword = ttk.Button(self.displayFrame, text="Update", style='Update.TButton', command=getNewSenderPassword)
            upd_mailPassword.grid(row = 2, column =2 )
            upd_receiverMail = ttk.Button(self.displayFrame, text="Update", style='Update.TButton', command=getNewReceiver)
            upd_receiverMail.grid(row=4, column=2)
            print('Flag1')
            upd_masterPassword = ttk.Button(self.displayFrame, text="Update", style='Update.TButton', command=getMasterPassword)
            upd_masterPassword.grid(row=6, column=2)


        except TypeError:
            pass
    displayContents()
