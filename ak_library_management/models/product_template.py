# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    """
    This model inherited the product template model
    In this model I added some custom fields and
    change the label of already exists barcode field
    """
    _inherit = "product.template"

    is_library_book = fields.Boolean(string="Is Library Book")
    author = fields.Char(string="Author Name")
    publisher = fields.Char(string="Publisher")
    edition = fields.Char(string="Book Edition")
    published_date = fields.Date(string="Published Date")
    pages = fields.Integer(string="Pages")
    available = fields.Boolean(string="Available In Stock")
    barcode = fields.Char(string="ISBN Number") # this field already in parent class I changed label of field
    status = fields.Selection(selection=[('available','Available'),('borrowed','Borrowed')],string="Status",default="available")

    def change_status(self):
        """This function change or set the status of the book availability"""
        if self.status == 'available':
            self.status = 'borrowed'
        else:
            self.status = 'available'
