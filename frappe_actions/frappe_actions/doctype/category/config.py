import frappe
from frappe import _
import re

# Define the validation method
def validate_my_doctype(doc, method):
    # Perform validation checks
    if not doc.is_active:
        frappe.throw(_("Field 'is_active' is required."))
    elif not isinstance(doc.is_active, bool):
        frappe.throw(_("'is_active' must be a boolean"))
    if not doc.title:
        frappe.throw(_("Field 'My Field' is required."))
    elif not re.match("^[a-zA-Z ]*$", doc.title):
        frappe.throw(_("'Title' field can only contain alphabets and spaces"))

# Attach the validation method to the doctype
def after_insert():
    doctype = "My Doctype"  # Replace with your doctype name
    frappe.get_doc("DocType", doctype).validate = validate_my_doctype

# Register the after_insert hook
def setup():
    frappe.db.after_insert("My Doctype", after_insert)

# Run setup function
if __name__ == "__main__":
    setup()