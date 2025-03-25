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
