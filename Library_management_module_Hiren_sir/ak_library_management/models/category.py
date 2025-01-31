# -*- coding: utf-8 -*-
#import models and fields from the odoo folder
from odoo import models,fields

class Category(models.Model):
    """
    	this is model for categories for books at library.
    	fields example:
    	field-name			example-value
    	name				fiction
    	tag_ids             many to many field where select multiple tags from the tag list
    """
    _name = "library.category"
    _description = "Library Category"

    name = fields.Char(string="Category Name")
    tag_ids = fields.Many2many('library.book.tags', 'book_tag_rel', 'category_id', 'tag_id', 'Tags')
