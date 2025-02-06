import frappe
from frappe.utils import getdate
from datetime import date, timedelta

week_days = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}


@frappe.whitelist()
def update_installments_status():
    installments = frappe.get_all(
        "Installments",
        fields=["name", "due_date", "status", "paid_amount", "amount"],
        filters=[["status", "=", "Not Paid"]],
    )

    for installment in installments:
        if date.today() > getdate(installment.due_date):
            frappe.db.set_value(
                "Installments",
                installment.name,
                "status",
                "Overdue",
            )


@frappe.whitelist()
def create_payment_installments():
    progress = 0
    customers = frappe.get_all(
        "Customer",
        fields=["name", "payment_day", "installments_frequency"],
        filters=[
            ["disabled", "=", 0],
            ["installments_count", ">", 0],
            ["payment_day", "!=", ""],
        ],
    )

    if len(customers) == 0:
        frappe.msgprint("No customers to create installments for")
        return

    for customer in customers:
        installments_count = frappe.db.count("Installments", filters=[["customer", "=", customer.name]])
        frappe.log(f"installments_count {installments_count}")

        if installments_count > 1:
            last_installment = frappe.get_last_doc(
                "Installments",
                filters=[
                    ["customer", "=", customer.name],
                    ["status", "!=", "Cancelled"]
                ]
            )
            if getdate(last_installment.next_installment) == getdate(frappe.utils.today()):
                frappe.log('Auto')
                new_installment_call(
                    customer=customer, progress=progress, customers_len=len(customers),
                    next_installment=last_installment.next_installment
                )
                return

        frappe.log('Manual')
        new_installment_call(
            customer=customer, progress=progress, customers_len=len(customers),
            next_installment=None
        )


def new_installment_call(customer, progress: int, customers_len: int, next_installment):
    due_date = date_for_weekday(week_days[customer.payment_day])
    sales_team = frappe.db.sql(
        f"""
            select
    	        sales_person
    	    from
    	        `tabSales Team`
    	    where
    		    parent = '{customer.name}'
            """
    )

    if len(sales_team) > 0:
        default_sales_team = sales_team[0]
        frappe.call(
            "payment_installments.payment_installments.doctype.installments.installments.new_installment",
            customer=customer.name,
            due_date=due_date,
            next_installment=frappe.utils.getdate(
                frappe.utils.add_days(
                    next_installment if next_installment else due_date,
                    customer.installments_frequency
                )
            ),
            sales_person=default_sales_team[0],
        )
        progress += 1 * 100 / customers_len
        frappe.publish_progress(progress, "Creating New Installments", description=customer.name)
    else:
        frappe.msgprint(
            f"Customer {customer.name} does not have a sales team or payment day"
        )


def date_for_weekday(day: int):
    today = date.today()
    # weekday returns the offsets 0-6
    # If you need 1-7, use isoweekday
    weekday = today.weekday()
    return today + timedelta(days=day - weekday)
