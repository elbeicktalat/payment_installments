app_name = "payment_installments"
app_title = "Payment Installments"
app_publisher = "Talat El Beick"
app_description = "Frappe add-on for adding Installment feature in Accounting"
app_email = "talatelbeick@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []
fixtures = [
    {"doctype": "Custom Field", "filters": [["module", "=", "Payment Installments"]]},
    {"doctype": "Client Script", "filters": [["module", "=", "Payment Installments"]]},
]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "payment_installments",
# 		"logo": "/assets/payment_installments/logo.png",
# 		"title": "Payment Installments",
# 		"route": "/payment_installments",
# 		"has_permission": "payment_installments.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/payment_installments/css/payment_installments.css"
# app_include_js = "/assets/payment_installments/js/payment_installments.js"

# include js, css files in header of web template
# web_include_css = "/assets/payment_installments/css/payment_installments.css"
# web_include_js = "/assets/payment_installments/js/payment_installments.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "payment_installments/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "payment_installments/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "payment_installments.utils.jinja_methods",
# 	"filters": "payment_installments.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "payment_installments.install.before_install"
# after_install = "payment_installments.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "payment_installments.uninstall.before_uninstall"
# after_uninstall = "payment_installments.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "payment_installments.utils.before_app_install"
# after_app_install = "payment_installments.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "payment_installments.utils.before_app_uninstall"
# after_app_uninstall = "payment_installments.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "payment_installments.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Sales Order": {
        "validate": "payment_installments.utils.validate_sales_order",
    },
    "Sales Invoice": {
        "validate": "payment_installments.utils.validate_sales_invoice",
    },
    "Customer": {
        "validate": "payment_installments.utils.validate_customer",
    },
}

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "payment_installments.tasks.update_installments_status",
    ],
    "weekly": [
        "payment_installments.tasks.create_payment_installments",
    ],
}

# scheduler_events = {
# 	"all": [
# 		"payment_installments.tasks.all"
# 	],
# 	"daily": [
# 		"payment_installments.tasks.daily"
# 	],
# 	"hourly": [
# 		"payment_installments.tasks.hourly"
# 	],
# 	"weekly": [
# 		"payment_installments.tasks.weekly"
# 	],
# 	"monthly": [
# 		"payment_installments.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "payment_installments.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "payment_installments.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "payment_installments.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["payment_installments.utils.before_request"]
# after_request = ["payment_installments.utils.after_request"]

# Job Events
# ----------
# before_job = ["payment_installments.utils.before_job"]
# after_job = ["payment_installments.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"payment_installments.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
