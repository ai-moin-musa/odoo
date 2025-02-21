# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BorrowTransactionHistory(models.Model):
    _name = "borrow.transaction.history"
    _description = "Borrow Books Transaction History"

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")
    books = fields.Many2many(comodel_name="product.template", string="Books", domain=[('is_library_book', '=', True)])
    borrow_start_date = fields.Datetime(string="Borrow Start Date", default=fields.Date.today(), required=True)
    borrow_end_date = fields.Datetime(string="Borrow End Date", required=True)
    deposit_amount = fields.Float(string="Deposit Amount")

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def _check_dates(self):
        if any(self.filtered(lambda rec: rec.borrow_start_date > rec.borrow_end_date)):
            raise ValidationError("Start Date must be before End Date.'")

    def action_pass(self):
        print("-----------------pass-------------")
