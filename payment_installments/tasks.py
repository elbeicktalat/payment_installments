import frappe
from datetime import date, timedelta

@frappe.whitelist()
def update_installments_status():
    installments = frappe.get_all(
        "Installments",
        fields=["name", "due_date", "status", "paid_amount", "amount"],
        filters=[["status", "=", "Not Paid"]],
    )

    for installment in installments:
        if installment.due_date < date.today():
            frappe.db.set_value(
                "Installments",
                installment.name,
                "status",
                "Overdue",
            )


@frappe.whitelist()
def create_payment_installments():
    progress = 0
    frappe.publish_progress(progress, "Creating New Installments")
    customers = frappe.get_all(
        "Customer",
        fields=["name", "payment_day"],
        filters=[
            ["disabled", "=", 0],
            ["installments_count", ">", 0],
            ["payment_day", "!=", ""],
        ],
    )

    if len(customers) == 0:
        frappe.msgprint("No customers to create installments for")
        return

    days = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    for customer in customers:
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
                due_date=date_for_weekday(days[customer.payment_day]),
                sales_person=default_sales_team[0],
            )
            progress += 1 * 100 / len(customers)
            frappe.publish_progress(progress, "Creating New Installments")
        else:
            frappe.msgprint(
                f"Customer {customer.name} does not have a sales team or payment day"
            )
    frappe.msgprint("Installments Created Successfully")


def date_for_weekday(day: int):
    today = date.today()
    # weekday returns the offsets 0-6
    # If you need 1-7, use isoweekday
    weekday = today.weekday()
    return today + timedelta(days=day - weekday)
