# -*- coding: utf-8 -*-
# import models and fields from the odoo folder
from odoo import models, fields


class LibraryLibrary(models.Model):
    """
        	this is model for libraries for books at multiple library.
        	fields example:
        	field-name			example-value
        	name				Library - 1
        	location            One Park (Location of the library)
        	capacity            5000 (capacity of storing books)
        	notes               This library has fiction books only
        	book_ids            This is One 2 many relationship with library.book model book_id field
        	product_ids         book can be product. I added this field for product.template model
        	                    many 2 many relation.
        """
    _name = "library.library"
    _description = "Library"

    name = fields.Char(string="Name", required=True)
    location = fields.Char(string="Location", required=True)
    capacity = fields.Integer(string="capacity")
    notes = fields.Text(string="Notes")
    book_ids = fields.One2many("library.book", "library_id", "Book")
    product_ids = fields.Many2many("product.template","library_product_rel",
                                   "library_id","product_id","Books",domain=[('is_library_book','=',True)])
