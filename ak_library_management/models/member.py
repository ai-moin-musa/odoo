# -*- coding: utf-8 -*-
from odoo import models,fields

class Member(models.Model):
    """
    	this is model for members at library.
    	fields example:
    	field-name			example-value
    	name				Robert
    	email				robert@example.com
    	phone				+91 8745693214
    	membership_date 	11/07/2008
    """
    _name = "library.member"
    _description = "Library Members"

    name = fields.Char(string="Name",required=True)
    email = fields.Char(string="Email ID")
    phone = fields.Char(string="Contact Number")
    membership_date = fields.Date(string="Start Date of Membership")
