from tkinter import *
from tkinter import messagebox, ttk
from config.dynamicSize import FR, WR, HR,availableFonts
from Frames.supportingFunctions import getConnect
from tkinter import font


def mailOptions(self, tab):
    def configureSettingsData(key, value):
        self.UpdatePopUp.destroy()

        collection = getConnect(self.activeDatabase, 'configuration')

        # For Cloud Atlas
        # client = MongoClient(
        #     "mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database(self.activeDatabase)
        # collection = db.configuration

        collection.find_one_and_update(
            {'_id': 'settingsData'}, {'$set': {key: value}})
        data = collection.find_one({'_id': 'settingsData'})
        self.sender_emaildata.config(text=data['sender_email'])
        self.receiver_emaildata.config(text=data['receiver_email'])
        self.master_passworddata.config(text=data['master_password'])
        self.sender_passworddata.config(text=data['sender_password'])
        self.currentFont.config(text=data['fontToUse'])
        self.currentDate.config(text=data['currentDateType'])

        messagebox.showinfo(
            'Value Updated', 'Value has been successfully Updated')

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
        configureSettingsData('master_password', value)

    def update_Font():
        value = self.comboboxToChooseFrom.get()
        configureSettingsData('fontToUse', value)

    def update_DateType():
        value = self.comboboxToChooseFrom.get()
        configureSettingsData('currentDateType', value)

    # Displays pop-Up to get new Values
    def displayTop(displayText, cmd, values=[]):
        self.UpdatePopUp = Toplevel()
        self.UpdatePopUp.grab_set()
        self.UpdatePopUp.title("Update Values")

        self.UpdatePopUp.geometry("+%d+%d" % (400, 300))
        # self.UpdatePopUp.minsize(200,200)

        updateLabel = Label(self.UpdatePopUp, text=displayText)
        updateLabel.grid(row=0, column=0, padx=10, pady=10)
        if len(values) != 0:
            self.comboboxToChooseFrom = ttk.Combobox(
                self.UpdatePopUp, values=values, state="readonly")
            self.comboboxToChooseFrom.grid(row=1, column=0, padx=20)
        else:
            self.AppsSettingsEntry = Entry(self.UpdatePopUp, width=20)
            self.AppsSettingsEntry.grid(row=1, column=0, padx=10, pady=10)
            self.AppsSettingsEntry.focus()
        updateBtn = Button(self.UpdatePopUp, text="Update", command=cmd)
        updateBtn.grid(row=2, column=0, padx=10, pady=20)

    # # Functions to Display pop up and get new values
    def getNewSender():
        displayTop('Enter New Sender Mmail-id', update_sender)

    def getNewSenderPassword():
        displayTop('Enter New Sender Password', update_senderPassword)

    def getNewReceiver():
        displayTop('Enter New Receiver Mail-id', update_receiver)

    def getMasterPassword():
        displayTop('Enter New Master Password', update_MasterPassword)

    def getDateType():
        displayTop('Choose the dateType', update_DateType, ['AD', 'BS'])

    def getFont():
        displayTop('Choose the font to Use',
                   update_Font, availableFonts)
    # Displays content in the App Settings Tab after authentyication

    def displayContents():
        try:
            # For local database storage
            collection = getConnect(self.activeDatabase, 'configuration')

            # For Cloud Atlas
            # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = client.get_database(self.activeDatabase)
            # collection = db.configuration

            sysData = collection.find_one({'_id': 'settingsData'})
            # connection.close()
            receiverLabel = Label(self.displayFrame, text=" Send mail using :", font=(
                self.fontToUse, int(FR*10), 'bold'))
            receiverLabel.grid(row=0, column=0, padx=10, pady=10, sticky='w')

            infoLabel = Label(self.displayFrame,
                              text=" (Set this email address send backup)")
            infoLabel.grid(row=1, column=0, columnspan=2,
                           padx=10, pady=0, sticky='w')

            self.sender_emaildata = Label(self.displayFrame, text=sysData['sender_email'], font=(
                self.fontToUse, int(FR*10), 'bold'))
            self.sender_emaildata.grid(row=0, column=1, padx=10, pady=10)

            senderPasswordLabel = Label(self.displayFrame, text=" Sender email password :", font=(
                self.fontToUse, int(FR*10), 'bold'))
            senderPasswordLabel.grid(
                row=2, column=0, padx=10, pady=10, sticky='w')

            infoLabel = Label(self.displayFrame,
                              text=" (Password of the sender's email address)")
            infoLabel.grid(row=3, column=0, columnspan=2,
                           padx=10, pady=0, sticky='w')

            self.sender_passworddata = Label(self.displayFrame, text='*********', font=(
                self.fontToUse, int(FR*10), 'bold'))  # sysData['sender_password']
            self.sender_passworddata.grid(row=2, column=1, padx=10, pady=10)

            receiverLabel = Label(self.displayFrame, text=" Receive mail in: ", font=(
                self.fontToUse, int(FR*10), 'bold'))
            receiverLabel.grid(row=4, column=0, padx=10, pady=10, sticky='w')

            infoLabel = Label(
                self.displayFrame, text=" (Set this email address to receive backup)")
            infoLabel.grid(row=5, column=0, columnspan=2,
                           padx=10, pady=0, sticky='w')

            self.receiver_emaildata = Label(
                self.displayFrame, text=sysData['sender_email'], font=(self.fontToUse, int(FR*10), 'bold'))
            self.receiver_emaildata.grid(row=4, column=1, padx=10, pady=10)

            masterPasswordLabel = Label(self.displayFrame, text="Master Password :", font=(
                self.fontToUse, int(FR*10), 'bold'))
            masterPasswordLabel.grid(
                row=6, column=0, padx=10, pady=10, sticky='w')

            self.master_passworddata = Label(
                self.displayFrame, text=sysData['master_password'], font=(self.fontToUse, int(FR*10), 'bold'))
            self.master_passworddata.grid(row=6, column=1, padx=10, pady=10)
            infoLabel = Label(self.displayFrame,
                              text=" (Password to access the Setting Tab)")
            infoLabel.grid(row=7, column=0, columnspan=2,
                           padx=10, pady=0, sticky='w')
            currentFontLabel = Label(self.displayFrame, text="Current Font", font=(
                self.fontToUse, int(FR*10), 'bold'))
            currentFontLabel.grid(
                row=8, column=0, padx=10, pady=10, sticky='w')

            infoLabel = Label(self.displayFrame,
                              text="(Font that is being used )")
            infoLabel.grid(row=9, column=0, columnspan=2,
                           padx=10, pady=0, sticky='w')

            self.currentFont = Label(self.displayFrame, text=sysData['fontToUse'], font=(
                self.fontToUse, int(FR*10), 'bold'))
            self.currentFont.grid(row=8, column=1, padx=10, pady=10)

            dateOptionsLabel = Label(self.displayFrame, text="Date Type Being Used", font=(
                self.fontToUse, int(FR*10), 'bold'))
            dateOptionsLabel.grid(
                row=10, column=0, padx=10, pady=10, sticky='w')

            infoLabel = Label(self.displayFrame,
                              text="(Date type that is being used )")
            infoLabel.grid(row=11, column=0, columnspan=2,
                           padx=10, pady=0, sticky='w')

            self.currentDate = Label(self.displayFrame, text=sysData['currentDateType'], font=(
                self.fontToUse, int(FR*10), 'bold'))
            self.currentDate.grid(row=10, column=1, padx=10, pady=10)

            upd_btn = ttk.Style()
            upd_btn.configure('Update.TButton', width=int(
                WR*10), font=('Times New Roman', int(FR*10)))

            upd_sendermail = ttk.Button(
                self.displayFrame, text="Update", style='Update.TButton', command=getNewSender)
            upd_sendermail.grid(row=0, column=2)

            upd_mailPassword = ttk.Button(
                self.displayFrame, text="Update", style='Update.TButton', command=getNewSenderPassword)
            upd_mailPassword.grid(row=2, column=2)
            upd_receiverMail = ttk.Button(
                self.displayFrame, text="Update", style='Update.TButton', command=getNewReceiver)
            upd_receiverMail.grid(row=4, column=2)
            upd_masterPassword = ttk.Button(
                self.displayFrame, text="Update", style='Update.TButton', command=getMasterPassword)
            upd_masterPassword.grid(row=6, column=2)
            upd_font = ttk.Button(
                self.displayFrame, text="Update", style='Update.TButton', command=getFont)
            upd_font.grid(row=8, column=2)
            upd_date = ttk.Button(
                self.displayFrame, text="Update", style='Update.TButton', command=getDateType)
            upd_date.grid(row=10, column=2)
        except TypeError:
            pass
    displayContents()
