// Copyright (c) 2025, Talat El Beick and contributors
// For license information, please see license.txt

frappe.ui.form.on("Installments", {
    refresh(frm) {
        const smartFillCallback = async () => {
            const today = new Date();
            const todayFormatted = getFormattedDate(today)

            if (frm.doc.customer === undefined) {
                frappe.throw("Please select a customer.")
                return
            }
            const customer = await frappe.db.get_doc("Customer", frm.doc.customer);
            const get_current_balance = await frappe.call({
                method: "erpnext.accounts.utils.get_balance_on",
                args: {date: todayFormatted, party_type: 'Customer', party: customer.name},
            });

            const current_balance = get_current_balance.message;

            if (current_balance === 0) {
                frappe.throw(`Customer ${customer.name} doesn't have any balance.`);
                return;
            }

            const sales_invoice = await frappe.db.get_list("Sales Invoice", {
                fields: ["customer_balance", "grand_total"],
                filters: [["customer", "=", customer.name]],
                order_by: 'creation desc',
                limit: 1,
            })
            const last_sales_invoice = sales_invoice[0];
            const rata = (Math.round((last_sales_invoice.customer_balance + last_sales_invoice.grand_total) / customer.installments_count / 500) * 500)

            if (rata > customer.minimum_installment_amount) {
                frm.set_value("amount", rata);
            } else if (customer.minimum_installment_amount < current_balance) {
                frm.set_value("amount", customer.minimum_installment_amount);
            } else {
                frm.set_value("amount", current_balance);
            }

            const dueDate = today.addDays(customer.installments_frequency);
            frm.set_value("due_date", getFormattedDate(dueDate));
            frm.set_value("next_installment", getFormattedDate(dueDate.addDays(customer.installments_frequency)));
        };
        frm.add_custom_button(__('Smart Fill'), smartFillCallback);

        frm.add_custom_button(__("Payment Entry"), () => {
            console.log('pay')
        }, __("Create"));

        frm.trigger("populate_summary_html");
    }, async populate_summary_html(frm) {

        if (frm.doc.customer === undefined) return;

        const customer = await frappe.db.get_doc("Customer", frm.doc.customer);
        const balance = await frappe.call({
            method: "erpnext.accounts.utils.get_balance_on", args: {
                date: (frm.doc.docstatus !== 0 ? getFormattedDate(new Date()) : frm.doc.creation),
                party_type: 'Customer',
                party: customer.name
            },
        });

        const sales_invoice = await frappe.db.get_list("Sales Invoice", {
            fields: ["customer_balance", "grand_total"],
            filters: [["customer", "=", customer.name]],
            order_by: 'creation desc',
            limit: 1,
        })
        const last_sales_invoice = sales_invoice[0];
        const rata = (Math.round((last_sales_invoice.customer_balance + last_sales_invoice.grand_total) / customer.installments_count / 500) * 500)


        console.log(customer)
        // Generate HTML
        const html = `
        <ul>
            <li><strong>Rata:</strong> ${format_currency(rata)}</li>
            <li><strong>Customer Balance:</strong> ${format_currency(balance.message)}</li>
            <li><strong>Last Invoice Total:</strong> ${format_currency(last_sales_invoice.grand_total)}</li>
            <li><strong>Preferred Payment Day:</strong> ${customer.payment_day}</li>
            <li><strong>Installments Frequency Evry:</strong> ${customer.installments_frequency} Days</li>
            <li><strong>Min Installments Amount:</strong> ${format_currency(customer.minimum_installment_amount)}</li>
        </ul>
    `;

        // Set the above `html` as Summary HTML
        frm.set_df_property("summary_html", "options", html);
    }
});

Date.prototype.addDays = function (days) {
    const date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

function getFormattedDate(date) {
    const dd = String(date.getDate()).padStart(2, '0');
    const mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
    const yyyy = date.getFullYear();
    return `${yyyy}-${mm}-${dd}`;
}