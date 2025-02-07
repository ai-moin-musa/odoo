# -*- coding: utf-8 -*-
# import models and fields from the odoo folder
from odoo import models, fields


class LibraryBook(models.Model):
    """
    this is model for book at library.
    fields example:
    field-name			example-value
    name				Rich dad poor dad
    author				Robert
    isbn				232-212-122
    publication_date	11/07/2008
    category_id			takes id from the category model example value: fiction
    description			this book for business
    state				available or borrowed
    tag_ids				it is related field ex: - Fiction, Science
    library_id			This is Many to one field of library.library model library_id field
    """
    _name = "library.book"
    _description = "Library Books"

    name = fields.Char(string="Book Title", required=True)
    author = fields.Char(string="Author Name")
    isbn = fields.Char(string="ISBN Number")
    publication_date = fields.Date(string="Date of Publication")
    category_id = fields.Many2one("library.book.category", "Book Category")
    description = fields.Text(string="Book Summary")
    state = fields.Selection(selection=[('available', "Available"), ("borrowed", "Borrowed")],
                             string="Book Availability", copy=False, default='available')
    tag_ids = fields.Many2many(related='category_id.tag_ids', string="Book Tags")
    library_id = fields.Many2one("library.library", "Library")
