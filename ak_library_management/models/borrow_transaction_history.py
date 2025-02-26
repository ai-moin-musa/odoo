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
    is_member = fields.Boolean(related="customer_id.is_member")
    deposit_amount = fields.Float(string="Deposit Amount")

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def _check_dates(self):
        if any(self.filtered(lambda rec: rec.borrow_start_date > rec.borrow_end_date)):
            raise ValidationError("Start Date must be before End Date.'")

    def action_confirm(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': "Warning",
            'res_model': 'borrow.books.checklist.wizard',
            'target': 'new',
            'view_mode': 'form',
            'context': {
                'default_message': "",
            }
        }

        for rec in self:
            if rec.customer_id.not_trust_worthy:
                action['context']['default_message'] = "Customer is not trustworthy. Are you sure you want to continue?"
                return action
            selected_book_ids_list = [single_rec.name for single_rec in rec.books if single_rec.qty_available == 0]
            if len(selected_book_ids_list) > 0:
                action['context'][
                    'default_message'] = f"The following books are out of stock: {selected_book_ids_list}. Are you sure you want to continue?"
                return action
            transactions = self.env['borrow.transaction.history'].search_count(
                [('customer_id', '=', rec.customer_id.id)])
            rec_sets = self.env['borrow.transaction.history'].search([('customer_id', '=', rec.customer_id.id)])
            books_count = sum([len(record.books) for record in rec_sets])
            if len(rec.books) > 5:
                if transactions > 1:
                    action['context'][
                        'default_message'] = f"Customer already has [{transactions - 1}] open borrow transactions with [{books_count - len(rec.books)}] books. Are you sure you want to borrow more books?"
                    return action
                else:
                    action['context'][
                        'default_message'] = f"Are you sure you want to allow borrowing more than 5 books for this customer?"
                    return action
