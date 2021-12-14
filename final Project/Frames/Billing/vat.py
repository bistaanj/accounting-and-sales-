from tkinter import messagebox
import Frames.Billing.viewProductsInBill as viewProductsInBill

def vat_billing(self,viewTree):
    if self.billing_method ==1:
        viewProductsInBill.viewProductsInBill(self,viewTree)
        if (self.billingTotalAmount != 0):
            validate = messagebox.askokcancel("Billing on Process","Do you want to swiitch to VAT Billing ? ")
            if (validate):
                self.productsInBill = {}
                self.billingTotalAmount = 0
                self.billingAmountLabel.config(text=self.billingTotalAmount)
                viewProductsInBill()
                self.billing_method = 0
                self.billtypelabel.config(text='VAT BILLING')
                self.billingVatableAmountLabel.grid(row=1, column=1, sticky="n",  pady=0)
                self.VatableAmountLabel.grid(row=1, column=0, sticky="n",  pady=0)
                self.billingVatableAmountLabel.config(text = 0)

                #templabel.grid_forget()
        else:
            self.billing_method = 0
            self.billtypelabel.config(text='VAT BILLING')
            self.billingVatableAmountLabel.grid(row=1, column=1, sticky="n",  pady=0)
            self.VatableAmountLabel.grid(row=1, column=0, sticky="n",  pady=0)
            self.billingVatableAmountLabel.config(text = 0)


            #templabel.grid_forget()
