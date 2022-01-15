# from _typeshed import NoneType
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk
from authentication import createEnterprise as ce
import pymongo
import smtplib
from config.dynamicSize import FR, WR, HR
import Frames.window as Window
from PIL import ImageTk, Image


class AuthUser(Tk):
    def __init__(self):
        super(AuthUser, self).__init__()
        self.title("Login")
        self.iconbitmap('./res/dsk.ico')
        self.geometry('400x500')
        self.configure(bg='#ffffff')

        self.minsize(400,400)
        self.maxsize(500,450)
        self.displayFrame = Frame(self, bg='#ffffff')
        self.displayFrame.pack( fill='both')
        companyLabel = Label(self.displayFrame, text='Inventory And Sales Management',
                             fg='#000000',bg = '#ffffff', font=('Helvetica',int(FR*15),'bold', 'underline'))
        companyLabel.pack(padx = 20,pady=5)
        self.detailsFrame = Frame(self.displayFrame, bg='#ffffff')
        self.detailsFrame.pack(pady = 20,padx = 20, fill = 'both')
        
        self.createLoginPage()

    def createLoginPage(self):
        connection = pymongo.MongoClient("localhost", 27017)
        database = connection['enterprise']
        collection = database['registeredEnterprise']
        reg_ent = collection.find()
        self.registeredNames = []
        for x in reg_ent:
            self.registeredNames.append(x['name'])
        
        self.registeredNames.insert(0,'--Select Enterprise--') 
        self.detailsFrame.destroy()
        self.detailsFrame = Frame(self.displayFrame, bg='#ffffff')
        self.detailsFrame.pack(pady = 20,padx = 20, fill = 'both')
        self.picFrame = Frame(self.detailsFrame, bg = '#ffffff')
        self.picFrame.pack()

        image = Image.open("./res/dsk.ico")
        test = ImageTk.PhotoImage(image)

        label1 = Label(self.picFrame,image=test, width = int(WR*150), height = int(HR*150), bg = '#ffffff')
        label1.image = test
        label1.pack()

        # companySelect = Label(self.detailsFrame, text='Select Company',
        #                      fg='#000000',bg = '#ffffff', font=('Helvetica',int(FR*10),'bold', 'underline'))
        # companySelect.pack(padx = 20,pady=5)

        createCompany = Button(self.detailsFrame, text='Add Enterprise', cursor="hand2", border=0,
                                bg='#ffffff', fg='red', font=('Helvetica', int(FR*10), 'underline'), command=self.createEnterpriseForm)
        createCompany.pack(padx=10, pady = 10)

        companySelect = ttk.Combobox(self.detailsFrame, values =self.registeredNames, state='readonly' ,
                             background = '#ffffff', font=('Helvetica',int(FR*10),'bold'))
        companySelect.pack(padx = 20,pady=5)
        companySelect.current(0)


        


        def clearPlaceHolder(event):
            password_entry.delete(0, 'end')

        passwordFrame = Frame(self.detailsFrame, bg = '#ffffff')
        passwordFrame.pack()

        image = Image.open('./res/lck.png')
        test = ImageTk.PhotoImage(image)
        locklbl = Label(passwordFrame, image=test, height = int(HR*50), width = int(WR*50), bg = '#ffffff' )
        locklbl.image = test
        locklbl.grid(row = 0, column = 0)

        password_entry = Entry(passwordFrame,border = 0,width = int(WR*15),font=('default',int(FR*12),), bg = '#f0f3f7')
        password_entry.grid(row = 0 , column = 1,padx = 2, pady = 10, sticky = 'w')
        password_entry.insert(0,"Enter Password")
        password_entry.bind('<FocusIn>', clearPlaceHolder)
        
        loginbutton = Button(self.detailsFrame,text='Get Access', border = 0,width = int(WR*15),bg='#151FC4',fg = '#ffffff',font=('Helvetica',int(FR*13),'bold'), command = lambda:self.checkPass(companySelect.get(),password_entry.get()) )
        loginbutton.pack(padx=10, pady = 10)
        loginbutton.bind("<Return>",self.checkPass)

        forgotPassword = Button(self.detailsFrame, text='Forgot Password ?', cursor="hand2", border=0,
                                bg='#ffffff', fg='red', font=('Helvetica', int(FR*10), 'underline'), command=self.saendPassword)
        forgotPassword.pack(padx=10, pady = 10)

        ##For local storage
        # connection = pymongo.MongoClient('localhost',27017)
        # dbs = connection['enterprise']
        # collection = dbs['registeredEnterpeise']

        ##For Cloud Atlas
        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database('saiRecords')
        # collection = db.configuration

        # self.accessCred used for forget password function aswell

        # self.accessCred=collection.find_one({'_id': 'settingsData'})
        # self.accessLoginKey = self.accessCred['master_password']
        # connection.close()

    def createEnterpriseForm(self):

        def collectData():
            name = eName_entry.get()
            password = password_entry.get() 
            dbsKey = databaseCreationKey.get()
            status=ce.addEnterprise(name,password,dbsKey)
            if (status):
                messagebox.showinfo('Successful Entry', 'New Enterprise Created Successfully. Please login')
                self.createLoginPage()
            else:
                messagebox.showerror('Invalid Entry', 'Please enter correct details.')
        
        for widget in self.detailsFrame.winfo_children():
            widget.destroy()
        
        eName = Label(self.detailsFrame, text = 'Name', bg = '#ffffff')
        eName.grid(row=0, column=0, padx= int(WR*10))

        eName_entry = Entry(self.detailsFrame,bg = '#f0f3f7')
        eName_entry.grid(row=0, column=1, padx= WR*10,pady=HR*10)

        eName = Label(self.detailsFrame, text = 'Password', bg = '#ffffff')
        eName.grid(row=1, column=0,padx= int(WR*10))

        password_entry = Entry(self.detailsFrame,bg = '#f0f3f7')
        password_entry.grid(row=1, column=1, padx= WR*10,pady=HR*10)

        esp_frame = Frame(self.detailsFrame, bg = '#ffffff')
        esp_frame.grid(row =2, column= 0 ,columnspan=2)

        espName = Label(esp_frame, text = 'Database Key', bg = '#ffffff')
        espName.grid(row=0, column=0)

        databaseCreationKey = Entry(esp_frame,bg = '#f0f3f7')
        databaseCreationKey.grid(row=0, column=1, padx= WR*8,pady=HR*10)

        inst_text = "Only alphabets. Do not enter especial characters."

        instruct = Label(esp_frame, text = inst_text, bg = '#ffffff', font=('Comic Sans MS', int(FR*8), 'underline'), fg = 'red')
        instruct.grid(row=1, column=0, columnspan= 2)


        submitButton = Button(self.detailsFrame,text='Create Enterprise', border = 0,width = int(WR*15),bg='#151FC4',fg = '#ffffff',font=('Helvetica',int(FR*13),'bold'), command = collectData)
        submitButton.grid(row=3, column=1, padx=WR*20, pady = HR*10)
        # submitButton.bind("<Return>",self.checkPass)




    def checkPass(self,name,key):
        connection = pymongo.MongoClient('localhost',27017)
        dbs = connection['enterprise']
        collection = dbs['registeredEnterprise']
        capturedData = collection.find_one({'name':name, 'password': key})
        
        try:
            self.activeDatabase= capturedData['key']
            
           # for online lisence authentication accessStatus is used
            accessStatus=1
            if (accessStatus):
                if (len(self.activeDatabase)>0):
                    self.destroy()
                    window = Window.Window(self.activeDatabase)
                    window.mainloop()
                
            else:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Access Denied", "Your Lisence is expired. Please Contact Developer. ")
            self.destroy()
        except ConnectionError:
            messagebox.showwarning("Connection Error", "Active Internet connection is required to validate Lisence.")
            self.destroy()
        except TypeError:
            messagebox.showerror("Access Denied", "Wrong Password. Please enter correct password ")


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
                messagebox.showinfo("Access Key Sent", "The Access Key has been sent to the registered email address.")


        except smtplib.socket.gaierror:
            messagebox.showerror("Connection Failed", 'This function requires active internet connection.')