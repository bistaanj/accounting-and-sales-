from tkinter import *
from tkinter import messagebox
from datetime import datetime
import pymongo
import smtplib
from config.dynamicSize import FR, WR, HR
from PIL import ImageTk, Image


class AuthUser(Tk):
    def __init__(self):
        super(AuthUser, self).__init__()
        self.title("Login")
        self.iconbitmap('./res/dsk.ico')
        self.geometry('600x600')

        self.minsize(500, 400)
        self.maxsize(550, 450)

        displayFrame = Frame(self, bg='#ffffff')
        displayFrame.pack(fill='both')

        companyLabel = Label(displayFrame, text='Regmi Electricals Centre',
                             fg='#000000', bg='#ffffff', font=('Helvetica', int(FR*25), 'bold', 'underline'))
        companyLabel.pack(padx=20, pady=5)

        detailsframe = Frame(displayFrame, bg='#ffffff')
        detailsframe.pack(pady=20, padx=20, fill='both')

        image = Image.open("./res/logo.jpg")
        test = ImageTk.PhotoImage(image)

        label1 = Label(detailsframe, image=test, width=int(
            WR*200), height=int(HR*200), bg='#ffffff')
        label1.image = test
        label1.pack()

        def clearPlaceHolder(event):
            self.password_entry.delete(0, 'end')

        passwordFrame = Frame(detailsframe, bg='#ffffff')
        passwordFrame.pack()

        image = Image.open('./res/lck.png')
        test = ImageTk.PhotoImage(image)
        locklbl = Label(passwordFrame, image=test, height=int(
            HR*50), width=int(WR*50), bg='#ffffff')
        locklbl.image = test
        locklbl.grid(row=0, column=0)

        self.password_entry = Entry(passwordFrame, border=0, width=int(
            WR*15), font=('default', int(FR*12),), bg='#f0f3f7')
        self.password_entry.grid(row=0, column=1, padx=2, pady=10, sticky='w')
        self.password_entry.insert(0, "Enter Password")
        self.password_entry.bind('<FocusIn>', clearPlaceHolder)
        self.password_entry.bind('<Return>', self.checkPass)

        loginbutton = Button(detailsframe, text='Get Access', border=0, width=int(
            WR*15), bg='#151FC4', fg='#ffffff', font=('Helvetica', int(FR*13), 'bold'), command=self.checkPass)
        loginbutton.pack(padx=10, pady=10)
        loginbutton.bind("<Return>", self.checkPass)

        forgotPassword = Button(detailsframe, text='Forgot Password ?', cursor="hand2", border=0,
                                bg='#ffffff', fg='red', font=('Helvetica', int(FR*10), 'underline'), command=self.saendPassword)
        forgotPassword.pack(padx=10, pady=10)

        # For local storage
        connection = pymongo.MongoClient('localhost', 27017)
        dbs = connection['saiRecords']
        collection = dbs['configuration']

        # For Cloud Atlas
        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.configuration

        self.accessCred = collection.find_one({'_id': 'settingsData'})
        self.accessLoginKey = self.accessCred['master_password']
        connection.close()

    def checkPass(self, event=''):
        try:
            # fbase = firebase.FirebaseApplication("https://sales-and-inventory-85242-default-rtdb.firebaseio.com/", None)
            # giveAccess = fbase.get('/sales-and-inventory-85242-default-rtdb:/appAuthentication', '')
            accessStatus = 1  # ;giveAccess['-MP5S3ILYqmOejEfu9Cp']['auth']
            if (accessStatus):
                key = self.password_entry.get()
                if (key == self.accessLoginKey):
                    self.destroy()
                    print("Hello")
                else:
                    messagebox.showerror(
                        "Invalid Key", "Wrong Password. Please enter correct password")
            else:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Access Denied", "Your Lisence is expired. Please Contact Developer. ")
            self.destroy()
        except ConnectionError:
            messagebox.showwarning(
                "Connection Error", "Active Internet connection is required to validate Lisence.")
            self.destroy()

    def saendPassword(self):
        try:
            nw = datetime.now()
            date = nw.strftime("%d/%m/%Y")
            time = nw.strftime("%H:%M")
            dte = date
            time = time
            validate = bool(0)
            validate = messagebox.askyesno(
                'Conformation Required', 'Do you want to send your password to the registered email address? ')
            if(validate):
                receiver_email = self.accessCred['receiver_email']
                password = self.accessCred['sender_password']
                sender_email = self.accessCred['sender_email']
                subject = "Access Key for the SaI Application "
                body = f' Kaligandaki Hardware \nYour Access Key is -  {self.accessLoginKey} \n Someone tried log in to the Software on {dte} at  {time} \n If this was not you, please consider conforming your staff'
                message = f'Subject: {subject}\n\n{body}'
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
                messagebox.showinfo(
                    "Access Key Sent", "The Access Key has been sent to the registered email address.")

        except smtplib.socket.gaierror:
            messagebox.showerror(
                "Connection Failed", 'This function requires active internet connection.')

    def __init__(self):
        super(AuthUser, self).__init__()
        # For local storage
        connection = pymongo.MongoClient('localhost', 27017)
        dbs = connection['saiRecords']
        collection = dbs['configuration']

        # For Cloud Atlas
        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.configuration

        self.accessCred = collection.find_one({'_id': 'settingsData'})
        print(self.accessCred)
        self.accessLoginKey = self.accessCred['master_password']
        connection.close()

    def checkPass(self, event=''):
        try:
            # fbase = firebase.FirebaseApplication("https://sales-and-inventory-85242-default-rtdb.firebaseio.com/", None)
            # giveAccess = fbase.get('/sales-and-inventory-85242-default-rtdb:/appAuthentication', '')
            accessStatus = 1  # ;giveAccess['-MP5S3ILYqmOejEfu9Cp']['auth']
            if (accessStatus):
                key = self.password_entry.get()
                if (key == self.accessLoginKey):
                    self.destroy()
                    return True
                else:
                    messagebox.showerror(
                        "Invalid Key", "Wrong Password. Please enter correct password")
            else:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Access Denied", "Your Lisence is expired. Please Contact Developer. ")
            self.destroy()
        except ConnectionError:
            messagebox.showwarning(
                "Connection Error", "Active Internet connection is required to validate Lisence.")
            self.destroy()

    def sendPassword(self):
        try:
            nw = datetime.now()
            date = nw.strftime("%d/%m/%Y")
            time = nw.strftime("%H:%M")
            dte = date
            time = time
            validate = bool(0)
            validate = messagebox.askyesno(
                'Conformation Required', 'Do you want to send your password to the registered email address? ')
            if(validate):
                receiver_email = self.accessCred['receiver_email']
                password = self.accessCred['sender_password']
                sender_email = self.accessCred['sender_email']
                subject = "Access Key for the SaI Application "
                body = f' Kaligandaki Hardware \nYour Access Key is -  {self.accessLoginKey} \n Someone tried log in to the Software on {dte} at  {time} \n If this was not you, please consider conforming your staff'
                message = f'Subject: {subject}\n\n{body}'
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
                messagebox.showinfo(
                    "Access Key Sent", "The Access Key has been sent to the registered email address.")

        except smtplib.socket.gaierror:
            messagebox.showerror(
                "Connection Failed", 'This function requires active internet connection.')
