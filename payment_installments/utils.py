import frappe

def validate_customer(self, arg):
    if self.installments_count is None:
        frappe.throw("Installments count must be set")
    elif self.installments_count < 1:
        frappe.throw("Installments count must be greater than 0")


def validate_sales_order(self, arg):
    balance = frappe.call(
        "erpnext.accounts.utils.get_balance_on",
        date=self.transaction_date,
        party_type="Customer",
        party=self.customer,
        company=self.company,
    )

    self.customer_balance = balance


def validate_sales_invoice(self, arg):
    balance = frappe.call(
        "erpnext.accounts.utils.get_balance_on",
        date=self.posting_date,
        party_type="Customer",
        party=self.customer,
        company=self.company,
    )

    self.customer_balance = balance
