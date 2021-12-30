from tkinter import *
from tkinter import messagebox
import pymongo
import smtplib

def dayEnd(self):
    try:
        # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.get_database(self.activeDatabase)
        # collection = db.configuration
        ##for local database
        connection = pymongo.MongoClient('localhost',27017)
        dbs = connection[self.activeDatabase]
        collection = dbs['configuration']
        sysData=collection.find_one({'_id': 'settingsData'})
        # collection = db.dailySalesData
        collection = dbs['dilySalesData']

        dateTime = self.getDateTime()
        dte = dateTime[0]
        time = dateTime[1]
        data = collection.find_one({'_id':dte})
        if data == None:
            raise ValueError
        amount = data['daySales']
        connection.close()
        validate = bool(0)
        validate=messagebox.askyesno('Conformation Required', 'Do you want to send the data?')
        if(validate):
            sender_email = sysData['sender_email']
            receiver_email = sysData['receiver_email']
            password = sysData['sender_password']
            subject = "Total sales for " + dte
            body = f' Kaligandaki Hardware \n Day Total Sales\n Date: {dte} \n Day End Time: {time} \n\n Daily Sales Amount for today is : {amount}'
            message = f'Subject: {subject}\n\n{body}'
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except ValueError:
        messagebox.showerror("Invalid Request","No Sales Made Yet.")
