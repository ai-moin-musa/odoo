# -*- coding: utf-8 -*-
#import models and fields from the odoo folder
from odoo import models,fields

class LibraryTags(models.Model):
    """
    	this is model for book at library.
    	fields example:
    	field-name			example-value
        name                magic
    """
    _name = "library.book.tags"
    _description = "Tags"

    name = fields.Char(string="Tag Name",required=True)
