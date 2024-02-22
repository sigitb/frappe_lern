import frappe
from frappe import _
import json


@frappe.whitelist(allow_guest=True)
def request_body(): 
    request_data = frappe.request.json

    # Perform data validation
    if not request_data:
        return _("Request data is missing"), 400  # Return error response if request data is missing

    # Example validation: Ensure 'key' field is present in the request data
    if 'key' not in request_data:
        return _("'key' field is required in the request data"), 400  # Return error response if 'key' field is missing

    # Process the request data
    # Example: Accessing a field named 'key' from the request body
    key_value = request_data.get('key')

    # Your API logic here
    return _("Received data: {}").format(key_value)

@frappe.whitelist(allow_guest=True)
def request_parmas():
    # Get request parameters
    params = frappe.form_dict

    # Example: Retrieve 'key' parameter from the request
    key_value = params.get('key')

    # Perform validation if needed
    if not key_value:
        return _("'key' parameter is required"), 400

    # Your API logic here
    return _("Received 'key' parameter: {}").format(key_value)

@frappe.whitelist(allow_guest=True)
def url_param(id):
    # 'id' will capture the value '1' from the URL path
    return frappe.db.sql("""SHOW DATABASES""");
    # Perform any additional logic here
    
    return _("Received parameter 'id': {}").format(id)

@frappe.whitelist(allow_guest=True)
def handle_put_request():
    if frappe.request.method != "PUT":
        return _("Method not allowed"), 405
    return _("Handling PUT request")


@frappe.whitelist(allow_guest=True)
def pagination():
    # Get pagination parameters from the request
    page = int(frappe.request.args.get('page', 1))
    page_size = int(frappe.request.args.get('page_size', 10))

    # Calculate the offset
    offset = (page - 1) * page_size

    # query_results = frappe.db.sql("""
    #     SELECT * FROM `tabAction`
    #     LIMIT %s, %s
    # """, (offset, page_size), as_dict=True)
    # total_records = frappe.db.sql("""
    #     SELECT COUNT(*) FROM `tabAction`
    # """)

    query_results = frappe.db.get_list("Action", fields=["title", "description","category.title as category_title", "category as category_collection"], limit=page_size, start=offset)
    total_records = frappe.db.count("Action")  # Calculate total number of records
    # return int(total_records[0][0]) 
    # Calculate total number of pages
    # total_pages = -(-int(total_records[0][0]) // page_size)
    total_pages = -(-int(total_records) // page_size)

    # Example response data including pagination metadata
    response_data = {
        "results": query_results,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_records": total_records,
            "total_pages": total_pages
        }
    }

    return response_data

@frappe.whitelist(allow_guest=True)
def register_user_via_website(email, password, first_name, last_name):    
    # Validasi alamat email
    if not frappe.utils.validate_email_address(email):
        return {"status": "failed", "message": "Alamat email tidak valid."}
    
    # Cek apakah alamat email sudah terdaftar
    if frappe.db.exists("User", email):
        return {"status": "failed", "message": "Alamat email sudah terdaftar."}
    
    
    
    try:
        # Buat pengguna baru
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        })
        
        # Set kata sandi
        user.set("password", password)

        user.insert(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "success", "message": "Pendaftaran berhasil. Silakan masuk."}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Registration Error"))
        return {"status": "failed", "message": "Terjadi kesalahan saat melakukan pendaftaran. Silakan coba lagi."}