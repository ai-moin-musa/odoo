# -*- coding: utf-8 -*-
#import models and fields from the odoo folder
from odoo import models,fields

class Book(models.Model):
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
	"""
	_name = "library.book"
	_description = "this is description of the model"

	name = fields.Char(string="Title")
	author = fields.Char(string="Author")
	isbn = fields.Char(string="ISBN")
	publication_date = fields.Date(string="Date of Publication")
	category_id = fields.Many2one("library.category","Category")
	description = fields.Text(string="Description")
	state = fields.Selection(selection=[('available',"Available"),("borrowed","Borrowed")],string="Status", copy=False, default='available')
