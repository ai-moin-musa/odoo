# -*- coding: utf-8 -*-
from odoo import models, fields


class LibraryBookCategory(models.Model):
    """
    this is model for categories for books at library.
    fields example:
    field-name			example-value
    name				fiction
    tag_ids             many to many field where select multiple tags
                        fromthe tag list
    """
    _name = "library.book.category"
    _description = "Library Category"

    name = fields.Char(string="Category Name", required=True)
    tag_ids = fields.Many2many('library.book.tags', 'book_tag_rel',
                               'category_id', 'tag_id', 'Tags')
