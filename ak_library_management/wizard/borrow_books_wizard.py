# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BorrowBooksWizard(models.TransientModel):
    _name = "borrow.books.wizard"
    _description = "Popup Borrow Books Wizard"

    customer_name = fields.Many2one(comodel_name="res.partner", string="Customer Name")
    from_datetime = fields.Datetime(string="From Datetime", default=fields.date.today(), required=True)
    end_datetime = fields.Datetime(string="End Datetime", required=True)
    book_ids = fields.Many2many(comodel_name="product.template", string="Books",
                                domain=[('is_library_book', '=', True)])
    is_member = fields.Boolean(related="customer_name.is_member")
    deposit_amount = fields.Float(string="Deposit Amount")

    @api.constrains('from_datetime', 'end_datetime')
    def _check_dates(self):
        if any(self.filtered(lambda rec: rec.from_datetime > rec.end_datetime)):
            raise ValidationError("Start Date must be before End Date.'")

    def action_confirm(self):
        for rec in self:
            if rec.customer_name.is_member:
                print(f"{rec.customer_name.name} is {rec.customer_name.is_member} member")

