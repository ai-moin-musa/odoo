# -*- coding: utf-8 -*-
#import models and fields from the odoo folder
from odoo import models,fields

class Category(models.Model):
    """
    	this is model for categories for books at library.
    	fields example:
    	field-name			example-value
    	name				fiction
    """
    _name = "library.category"
    _description = "library category"

    name = fields.Char(string="Category Name")
