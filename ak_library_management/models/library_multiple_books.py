# -*- coding: utf-8 -*-
# import models and fields from the odoo folder
from odoo import models, fields, api


class LibraryMultipleBooks(models.TransientModel):
    """
    pass
    """
    _name = "library.multiple.books"
    _description = "Library Multiple Books"

    book_names = fields.Text(string="Book Names")
    author = fields.Many2one("res.partner", "Author")
    category = fields.Many2one("library.book.category", "Books category",
                               default= lambda self: self.env['library.book.category'].search([], limit=1).id)
    price = fields.Integer(string="price", default=0)


    def create_products(self):
        print("created..............")

    def revert_changes(self):
        print("===========revert changes")
