# Copyright (c) 2025, Talat El Beick and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe import utils
from frappe.model.document import Document


class Installments(Document):
    def validate(self):
        pass


@frappe.whitelist()
def new_installment(
        customer: str, due_date: datetime.date, next_installment: datetime.date, sales_person: str,
        customer_address: str
):
    try:
        amount: int = 0
        customer = frappe.get_doc("Customer", customer)
        current_balance = frappe.call(
            "erpnext.accounts.utils.get_balance_on",
            date=frappe.utils.today(),
            party_type="Customer",
            party=customer.name,
        )

        if current_balance > 0:
            last_sales_invoice = frappe.get_last_doc(
                "Sales Invoice", filters={"customer": customer.name}
            )

            rata = (
                    round(
                        (last_sales_invoice.customer_balance + last_sales_invoice.grand_total)
                        / customer.installments_count
                        / 500
                    )
                    * 500
            )

            if rata > customer.minimum_installment_amount:
                amount = rata
            elif customer.minimum_installment_amount < current_balance:
                amount = customer.minimum_installment_amount
            else:
                amount = current_balance

            doc = frappe.get_doc(
                {
                    "doctype": "Installments",
                    "customer": customer.name,
                    "due_date": due_date,
                    "next_installment": next_installment,
                    "sales_person": sales_person,
                    "customer_address": customer_address,
                    "amount": amount,
                }
            )
            doc.insert()
            doc.submit()

            return doc
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"{e}")
        frappe.local.response["http_status_code"] = 500
        frappe.throw(e)


@frappe.whitelist()
def pay_installment(name: str, amount: float):
    try:

        doc = frappe.get_doc("Installments", name)
        sales_person = frappe.get_doc("Sales Person", doc.sales_person)

        if doc.paid_amount > 0:
            frappe.throw("Installment already paid")

        if amount > doc.amount:
            frappe.throw(
                f"Amount `{amount}` is greater than the installment amount `{doc.amount}`"
            )

        doc.paid_amount += amount

        if doc.paid_amount == doc.amount:
            doc.status = "Paid (Not Validated)"
        elif doc.paid_amount < doc.amount:
            doc.status = "Partly Paid (Not Validated)"

        pe = make_payment_entry(
            party=doc.customer,
            amount=amount,
            account=sales_person.cash_in_hand_account,
            contact=doc.contact_person,
        )

        doc.payment_entry = pe.name

        doc.save()
        frappe.db.commit()

        return doc
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"{e}")
        frappe.local.response["http_status_code"] = 500
        frappe.throw(e)


def make_payment_entry(party: str, amount: float, account: str, contact: str):
    try:
        doc = frappe.get_doc(
            {
                "doctype": "Payment Entry",
                "posting_date": frappe.utils.today(),
                "payment_type": "Receive",
                "party_type": "Customer",
                "party": party,
                "paid_to": account,
                "paid_amount": amount,
                "received_amount": amount,
                "contact_person": contact,
            }
        )

        doc.insert()
        doc.submit()
        frappe.db.commit()

        return doc
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"{e}")
        frappe.local.response["http_status_code"] = 500
        frappe.throw(e)
