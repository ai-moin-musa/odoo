# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
    _rec_name = "member_id"

    member_id = fields.Many2one(comodel_name='res.partner', string='Member Name', required=True)
    email = fields.Char(string="Email ID")
    phone = fields.Char(string="Contact Number")
    membership_date = fields.Date(string="Membership Start Date")
    membership_no = fields.Char(string="Membership Number",readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        """
        I override this method for set the membership_no value by sequence
        """
        for val in vals_list:
            val['membership_no'] = self.env['ir.sequence'].next_by_code('library.member')
        res = super().create(vals_list)
        return res

    def action_send_renewal_mail(self):
        """
        this action button method for sending renewl membership mail to the library member.
        """
        mail_template = self.env.ref('ak_library_management.email_template_renewal_membership')
        context = {
            'default_template_id': mail_template.id
        }
        if self.env.user.is_librarian:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'target': 'new',
                'context': context,
            }
        raise ValidationError("Only Librarian can send email!!! Contact to the Librarian.")
