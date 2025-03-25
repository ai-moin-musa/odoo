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
        # decrease the quantity of the books when transaction is completed
        for rec in self.books:
            if rec.qty_available:
                product_id = self.env['product.product'].search([('name', '=', rec.name),
                                                                 ('default_code', '=', rec.default_code)])
                loc = self.env['stock.quant'].search([('product_id.name', '=', rec.name)], limit=1)
                self.env['stock.quant']._update_available_quantity(product_id, loc.location_id,
                                                                   quantity=-1)

    def show_warning_wizard(self, name=None, message=None, step=1):
        view_id = self.env.ref('ak_library_management.borrow_books_checklist_wizard_view_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'res_model': 'borrow.transaction.history.wizard',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'context': {
                'default_message': message,
                'wizard_step': step,
                'default_customer_id': self.customer_id.id,
                'default_books': self.books.ids,
                'default_deposit_amount': self.deposit_amount,
                'default_borrow_end_date': self.borrow_end_date,
                'final_step': step
            }
        }

    def action_confirm(self):
        step = self.env.context.get('wizard_step', 1)
        if step == 1 and self.customer_id.not_trust_worthy:
            return self.show_warning_wizard(
                name="Borrowed Book",
                message="Customer is not trustworthy. Are you sure you want to continue?",
                step=2)

        if step <= 2:
            low_quantity_product = [rec.name for rec in self.books if rec.qty_available == 0]
            if low_quantity_product:
                return self.show_warning_wizard(
                    name="Low Quantity Warning",
                    message=f"The following books are out of stock: "
                            f"{', '.join(low_quantity_product)}. Are you sure?",
                    step=3)

        if step <= 3 and len(self.books) > 5:
            return self.check_borrowed_book_limit()

        return self.create_borrow_transaction()

    def create_borrow_transaction(self):
        self.env['borrow.transaction.history'].create({
            'customer_id': self.customer_id.id,
            'books': self.books.ids,
            'deposit_amount': self.deposit_amount,
            'borrow_start_date': self.borrow_start_date,
            'borrow_end_date': self.borrow_end_date
        })
        return self.decrease_quantity_of_product()

    def action_cancel(self):
        rec = self.env.context.get('active_id')
        self.env["borrow.transaction.history.wizard"].browse(rec).unlink()

    def check_borrowed_book_limit(self):
        search_record = self.env['borrow.transaction.history'].search(
            [('customer_id', "=", self.customer_id.id)])
        books = list(search_record[:-1].mapped("books").filtered(
            lambda book: book.name).mapped("name"))
        if books:
            name = "Warning Wizard"
            message = (f"{self.customer_id.name} already has {books}"
                       f"open borrow transactions with {len(self.books)} books."
                       "Are you want to borrow more books?")
            return self.show_warning_wizard(name, message, step=4)

        return self.show_warning_wizard(
            "Warning Wizard",
            "Are you want to allow borrowing more than 5 books for this customer?",
            step=4,
        )
