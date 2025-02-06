# -*- coding: utf-8 -*-
from odoo import models,fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_library_book = fields.Boolean(string="Is Library Book")
    author = fields.Char(string="Author Name")
    publisher = fields.Char(string="Publisher")
    edition = fields.Char(string="Book Edition")
    publisher_date = fields.Date(string="Published Date")
    pages = fields.Integer(string="Pages")
    available = fields.Boolean(string="Available In Stock")
    barcode = fields.Char(string="ISBN Number")
