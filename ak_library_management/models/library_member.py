# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LibraryMember(models.Model):
    """
    this is model for members at library.
    fields example:
    field-name			example-value
    name				Robert
    email				robert@example.com
    phone				+91 8745693214
    membership_date 	11/07/2008
    membership_no       MEM-2025-001 (This value set by the sequence)
    """
    _name = "library.member"
    _description = "Library Members"

    name = fields.Char(string="Member Name", required=True)
    email = fields.Char(string="Email ID")
    phone = fields.Char(string="Contact Number")
    membership_date = fields.Date(string="Membership Start Date")
    membership_no = fields.Char(string="Membership Number",readonly=True)

    @api.model_create_multi
    def create(self, vals):
        """
        I override this method for set the membership_no value by sequence
        """
        vals[0]['membership_no'] = self.env['ir.sequence'].next_by_code('library.member')
        res = super().create(vals)
        return res
