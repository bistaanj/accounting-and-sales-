from tkinter import messagebox
from tkinter.constants import END
import Frames.Billing.viewProductsInBill as viewProductsInBill


def order(self, viewTree):
    if self.billing_method == 0:
        viewProductsInBill.viewProductsInBill(self, viewTree)
        if (self.billingTotalAmount != 0):
            validate = messagebox.askokcancel(
                "Billing on Process", "Do you want to swiitch to Order ? ")
            if (validate):
                self.productsInBill = {}
                self.billingTotalAmount = 0
                self.billingAmountLabel.config(text=self.billingTotalAmount)
                viewProductsInBill.viewProductsInBill(self, viewTree)
                self.billing_method = 1
                #templabel.grid(row= 1,column=6)
                self.itemlistbox.delete(0, END)
                self.billtypelabel.config(text='Order')
                self.billingVatableAmountLabel.grid_forget()
                self.VatableAmountLabel.grid_forget()
        else:
            self.billing_method = 1
            self.billtypelabel.config(text='Order')
            #templabel.grid(row= 1,column=6)
            self.billingVatableAmountLabel.grid_forget()
            self.VatableAmountLabel.grid_forget()
