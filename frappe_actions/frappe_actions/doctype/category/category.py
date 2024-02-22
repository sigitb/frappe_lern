# Copyright (c) 2024, sigit and contributors
# For license information, please see license.txt

# import frappe
import frappe
import re
from frappe.model.document import Document


class Category(Document):
	def validate(self):
		self.validate_title()
		# self.validate_is_active()

	def validate_title(self):
		if not self.title:
			frappe.throw("Title tidak boleh kosong.")
		elif not re.match("^[a-zA-Z ]*$", self.title):
			frappe.throw("'Title' field can only contain alphabets and spaces")

	# def validate_is_active(self):
	# 	if not self.is_active:
	# 		frappe.throw("Field 'is_active' is required.")
		

	def after_insert(self):
		self.update_response("Created successfully")

	def update_response(self,error_message):
		self.response_message = error_message
	
	def on_update(self):
		self.update_response("Updated successfully")

	def on_trash(self):
		self.update_response("Deleted successfully")
