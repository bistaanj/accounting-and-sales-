from tkinter.constants import END


def viewProductsInBill(self, viewTree):
    count = 0
    self.billingTotalAmount = 0
    for rows in viewTree.get_children():
        viewTree.delete(rows)

    for values in self.productsInBill:
        viewTree.insert(parent='', index=END, iid=(self.productsInBill[values]['iid']),
                        text=(count+1),
                        values=(values,
                                self.productsInBill[values]['Quantity'],
                                self.productsInBill[values]['Units'],
                                self.productsInBill[values]['Sales Price'],
                                self.productsInBill[values]['Product Total']
                                ))
        self.billingTotalAmount += int(
            self.productsInBill[values]['Product Total'])
        self.billingAmountLabel.config(text=self.billingTotalAmount)

        self.billingAmountLabel.focus()

        if self.billing_method == 0:
            self.billingVatableAmountLabel.config(
                text=int(self.billingTotalAmount))
            self.billingAmountLabel.config(
                text=int(self.billingTotalAmount+0.13*self.billingTotalAmount))

        count += 1
    print('Products in Bill')
    print(self.productsInBill)
    self.executing = False
