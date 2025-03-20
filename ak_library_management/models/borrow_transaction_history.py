# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BorrowTransactionHistory(models.Model):
    _name = "borrow.transaction.history"
    _description = "Borrow Books Transaction History"
    _rec_name = 'customer_id'
    _inherit = 'res.config.settings'

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer")
    books = fields.Many2many(
        comodel_name="product.template",
        string="Books",
        domain=[('is_library_book', '=', True)]
    )
    borrow_start_date = fields.Date(
        string="Borrow Start Date",
        default=fields.Date.today(),
        required=True)
    borrow_end_date = fields.Date(string="Borrow End Date", required=True)
    is_member = fields.Boolean(related="customer_id.is_member")
    deposit_amount = fields.Float(string="Deposit Amount")
    is_active = fields.Boolean(compute="_compute_active_transaction",store=True)
    is_higher_than_limit = fields.Boolean(compute='_compute_more_than_borrow_limit', store=True)

    @api.depends('books')
    def _compute_more_than_borrow_limit(self):
        """
        this method used for checking customer open borrow transaction or not and restricts
        customer to borrow books more than borrow limit
        """
        for rec in self:
            rec.is_higher_than_limit = False
            records = self.search([('customer_id.id', "=", self.customer_id.id)])
            books_name = [book.name for rec in records
                          for book in rec.books]
            if len(books_name) > rec.borrow_limit:
                rec.is_higher_than_limit = True

    @api.depends('borrow_end_date')
    def _compute_active_transaction(self):
        """
        check the transaction is active or not.
        """
        for rec in self:
            rec.is_active = rec.borrow_end_date >= date.today()

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
        the confirm button checks some condition on basis
        of the customer and books he borrowed and return wizard
        with different messages based upon condition.
        :params: None
        :return: action dictionary
        :rtype: dict
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
                    "Customer is not trustworthy."
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

                action['context'][
                    'default_message'] = ("Are you sure you want to"
                                          "allow borrowing more than 5 books"
                                          "for this customer?")
                return action

            # decrease the quantity of the books when transaction is completed
            for rec in self.books:
                if rec.qty_available:
                    product_id = self.env['product.product'].search([('name', '=', rec.name),
                                                                     ('default_code', '=', rec.default_code)])
                    loc = self.env['stock.quant'].search([('product_id.name', '=', rec.name)], limit=1)
                    self.env['stock.quant']._update_available_quantity(product_id, loc.location_id,
                                                                       quantity=-1)

    def book_returned_reminder(self):
        """
        this method used for schedule action which is send notification on reminder
        book return date.
        """
        borrow_transaction_book_ids = self.search([('borrow_end_date', '<=', date.today()),
                                 ('books.status', '=', 'borrowed')])
        for rec in borrow_transaction_book_ids:
            mail_template = self.env.ref(
                'ak_library_management.email_template_library_book_reminder')
            mail_template.send_mail(rec.id, force_send=True)

    def automated_action_overdue_books(self):
        """
        This method used for customer cant borrow book without returning old books
        which is overdue of return date.
        """
        recs = self.search([('customer_id.id', "=", self.customer_id.id)])
        for rec in recs:
            for book in rec.books:
                if rec.borrow_end_date < date.today() and book.status == "borrowed":
                    raise ValidationError(f"{rec.customer_id.name}"
                                          f"with overdue books"
                                          f"cannot borrow new ones until"
                                          f"you return the overdue items.")
