# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BorrowTransactionHistoryWizard(models.TransientModel):
    """
    this class used to create an object for popup at product template so
    user can create transaction from the product template all fields same
    as Borrow Transaction History Model.
    """
    _name = "borrow.transaction.history.wizard"
    _description = "Borrow Transaction History Wizard"
    _rec_name = "customer_id"

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
    message = fields.Char(readonly=True)

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def _check_dates(self):
        """
        this method checks the end date is not before the start date
        """
        if any(self.filtered(lambda rec: rec.borrow_start_date > rec.borrow_end_date)):
            raise ValidationError("Start Date must be before End Date.'")

    def decrease_quantity_of_product(self):
        """
        decrease the quantity of the books when transaction is completed
        """
        for rec in self.books:
            if rec.qty_available:
                product_id = self.env['product.product'].search([('name', '=', rec.name),
                                                                 ('default_code', '=', rec.default_code)])
                loc = self.env['stock.quant'].search([('product_id.name', '=', rec.name)], limit=1)
                self.env['stock.quant']._update_available_quantity(product_id, loc.location_id,
                                                                   quantity=-1)

    def show_warning_wizard(self, name=None, message=None, context=None):
        """
        this method is get the parameter and update the context and modify the action
        and return it.
        :param name: wizard name
        :param message: wizard message
        :param context: action context
        :return: action dictionary
        :rtype: dict
        """
        view_id = self.env.ref('ak_library_management.borrow_books_checklist_wizard_view_form').id
        action = {
            'type': 'ir.actions.act_window',
            'name': name,
            'res_model': 'borrow.transaction.history.wizard',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'context': {
                'default_message': message,
                'default_customer_id': self.customer_id.id,
                'default_books': self.books.ids,
                'default_deposit_amount': self.deposit_amount,
                'default_borrow_end_date': self.borrow_end_date,
            }
        }
        action['context'].update(context)
        return action

    def action_confirm(self):
        """
        this method used to whenever user confirm the borrowed books transaction.
        and check the validation and return wizard according to validation.
        and after that create record of borrowed books transaction and decrease the
        quantity of product.
        """
        if self.env.context.get("not_trust_worthy", True) and self.customer_id.not_trust_worthy:
            return self.show_warning_wizard(
                name="Borrowed Book",
                message="Customer is not trustworthy. Are you sure you want to continue?",
                context={
                    'not_trust_worthy': False,
                    'low_quantity_product': True,
                    'check_borrowed_books': True,
                })
        if self.env.context.get("low_quantity_product", True):
            low_quantity_product = [rec.name for rec in self.books if rec.qty_available == 0]
            if low_quantity_product:
                return self.show_warning_wizard(
                    name="Low Quantity Warning",
                    message=f"The following books are out of stock: "
                            f"{', '.join(low_quantity_product)}. Are you sure?",
                    context={
                        'not_trust_worthy': False,
                        'low_quantity_product': False,
                        'check_borrowed_books': True,
                    })
        if self.env.context.get("check_borrowed_books", True) and len(self.books) > 5:
            return self.check_borrowed_book_limit()
        return self.create_borrow_transaction()

    def create_borrow_transaction(self):
        """
        this method creating record of borrow transaction history
        and decrease the quantity of the books.
        """
        self.env['borrow.transaction.history'].create({
            'customer_id': self.customer_id.id,
            'books': self.books.ids,
            'deposit_amount': self.deposit_amount,
            'borrow_start_date': self.borrow_start_date,
            'borrow_end_date': self.borrow_end_date
        })
        return self.decrease_quantity_of_product()

    def action_cancel(self):
        """
        this method revert the record of borrow transaction
        """
        rec = self.env.context.get('active_id')
        self.env["borrow.transaction.history.wizard"].browse(rec).unlink()

    def check_borrowed_book_limit(self):
        """
        this method checked the customer borrow book limit and if customer
        borrow books over the limit then return wizard or popup for warning
        of the over limit.
        :return: wizard (function)
        """
        search_record = self.env['borrow.transaction.history'].search(
            [('customer_id', "=", self.customer_id.id)])
        books = list(search_record[:-1].mapped("books").filtered(
            lambda book: book.name).mapped("name"))
        name = "Warning Wizard"
        message = "Are you want to allow borrowing more than 5 books for this customer?"
        if books:
            message = (f"{self.customer_id.name} already has {books}"
                       f"open borrow transactions with {len(self.books)} books."
                       "Are you want to borrow more books?")
        return self.show_warning_wizard(name, message, context={
            'not_trust_worthy': False,
            'low_quantity_product': False,
            'check_borrowed_books': False,
        })
