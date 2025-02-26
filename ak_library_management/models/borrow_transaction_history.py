# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BorrowTransactionHistory(models.Model):
    _name = "borrow.transaction.history"
    _description = "Borrow Books Transaction History"

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")
    books = fields.Many2many(
        comodel_name="product.template",
        string="Books",
        domain=[('is_library_book', '=', True)]
    )
    borrow_start_date = fields.Datetime(
        string="Borrow Start Date",
        default=fields.Date.today(),
        required=True)
    borrow_end_date = fields.Datetime(string="Borrow End Date", required=True)
    is_member = fields.Boolean(related="customer_id.is_member")
    deposit_amount = fields.Float(string="Deposit Amount")

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def _check_dates(self):
        """
        this method checks the end date is not before the start date
        """
        if any(self.filtered(lambda rec: rec.borrow_start_date > rec.borrow_end_date)):
            raise ValidationError("Start Date must be before End Date.'")

    def action_confirm(self):
        """
        this method for confirm button when user clicked on
        the confirm button checks the some condition on basis
        of the customer and books he borrowed and return wizard
        with different messages based upon condition.
        """
        # This modified action for borrow books wizard
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
            # checks the customer is trust worthy or not
            if rec.customer_id.not_trust_worthy:
                action['context']['default_message'] = (
                    "Customer is not trustworthy. "
                    "Are you sure you want to continue?")
                return action
            selected_book_ids_list = [
                single_rec.name for single_rec in rec.books if single_rec.qty_available == 0]
            # check if any book is out of stock
            if len(selected_book_ids_list) > 0:
                action['context'][
                    'default_message'] = (f"The following books are out of stock: "
                                          f"{selected_book_ids_list}. "
                                          f"Are you sure you want to continue?")
                return action
            # getting transactions records from the borrow transaction history model
            transactions = self.env['borrow.transaction.history'].search_count(
                [('customer_id', '=', rec.customer_id.id)])
            rec_sets = (self.env['borrow.transaction.history']
                        .search([('customer_id', '=', rec.customer_id.id)]))
            books_count = sum([len(record.books) for record in rec_sets])
            # check the customer selected more than five books or not
            if len(rec.books) > 5:
                if transactions > 1:
                    action['context'][
                        'default_message'] = (f"Customer already has "
                                              f"[{transactions - 1}] open borrow transactions with "
                                              f"[{books_count - len(rec.books)}] books. "
                                              f"Are you sure you want to borrow more books?")
                    return action
                else:
                    action['context'][
                        'default_message'] = (f"Are you sure you want to "
                                              f"allow borrowing more than 5 books "
                                              f"for this customer?")
                    return action

            # decrease the quantity of the books when transaction is completed
            for record in self.books:
                if record.qty_available:
                    record.qty_available -= 1



