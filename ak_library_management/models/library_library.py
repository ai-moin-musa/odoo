# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LibraryLibrary(models.Model):
    """
    this is model for libraries for books at multiple library.
    fields example:
    field-name			example-value
    name				Library - 1
    location            One Park (Location of the library)
    capacity            5000 (capacity of storing books)
    notes               This library has fiction books only
    book_ids            This is One 2 many relationship with library.
                        book model book_id field
    product_ids         book can be product. I added this field for product.
                        template model many 2 many relation.
    """
    _name = "library.library"
    _description = "Library"

    name = fields.Char(string="Name", required=True)
    location = fields.Char(string="Location", required=True)
    capacity = fields.Integer(string="capacity")
    notes = fields.Text(string="Notes")
    book_ids = fields.One2many("library.book", "library_id", "Book")
    product_ids = fields.Many2many("product.template", "library_product_rel",
                                   "library_id", "product_id", "Books",
                                   domain=[('is_library_book', '=', True)])
    borrowed_book_count = fields.Integer(
        string="Borrowed Book Count",
        compute="_compute_borrowed_books_count")

    @api.depends("product_ids")
    def _compute_borrowed_books_count(self):
        """
        this function count the number of books borrowed
        from the current library
        """
        self.borrowed_book_count = self.env['product.template'].search_count(
            [("status", "=", "borrowed"), ("id", "in", self.product_ids.ids)])

    def borrowed_books(self):
        """ this function returned filtered view of the borrowed books"""
        return {
            'name': 'Borrowed Books',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'product.template',
            'domain': [
                ('status', '=', 'borrowed'),
                ('id', 'in', self.product_ids.ids)
            ],
        }
