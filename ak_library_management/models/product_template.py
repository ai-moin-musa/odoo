# -*- coding: utf-8 -*-
from datetime import date, timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    """
    This model inherited the product template model
    In this model I added some custom fields and
    change the label of already exists barcode field
    """
    _inherit = "product.template"

    is_library_book = fields.Boolean(string="Is Library Book")
    author = fields.Char(string="Author Name")
    publisher = fields.Char(string="Publisher")
    edition = fields.Char(string="Book Edition")
    published_date = fields.Date(string="Published Date")
    pages = fields.Integer(string="Pages")
    available = fields.Boolean(string="Available In Stock")
    # this field already in parent class I changed label of field
    barcode = fields.Char(string="ISBN Number")
    status = fields.Selection(
        selection=[('available', 'Available'), ('borrowed', 'Borrowed'), ('returned', 'Returned')],
        string="Status",
        tracking=True)
    due_date = fields.Date(default=date.today())

    def mark_as_available(self):
        """This function change or set the status of the book availability"""
        self.status = "available"

    def mark_as_borrowed(self):
        """This is method for status change available to borrowed"""
        self.status = "borrowed"

    @api.model_create_multi
    def create(self, vals_list):
        """
        I override this method for set the reference value by sequence
        """
        for val in vals_list:
            val['default_code'] = self.env['ir.sequence'].next_by_code('product.template')
        res = super().create(vals_list)
        return res

    def action_borrow_books_wizard(self):
        """
        this method for opening or popup borrow books wizard
        for customer borrow books from this wizard
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrow Books Transaction History',
            'res_model': 'borrow.transaction.history',
            'target': 'new',
            'view_mode': 'form',
        }

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """this method for user can search by author name and name both."""
        args = list(args or [])
        if name:
            args += ['|', ('name', operator, name), ('author', operator, name)]
        return super().name_search(args=args, limit=limit)

    @api.depends('name', 'author')
    def _compute_display_name(self):
        """
        this method _compute_display_name for the
        created custom display name.
        """
        for rec in self:
            if rec._context.get('author_book'):
                rec.display_name = f"[{rec.author}]{rec.name}"
            else:
                rec.display_name = rec.name

    @api.constrains('status')
    def _check_status(self):
        """
        This _check_status constraints method check all the
        conditions and sends notifications and logs messages
        """
        # check the returning day
        if self.status == 'returned' and date.today() <= self.due_date:
            raise ValidationError(f"You can not Returned the Book before {self.due_date}")
        elif self.status != False:
            self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                'type': 'warning',
                'message': f"{self.name} book status is changed to {self.status}",
            })

        # creating schedule activity and send log message for borrow books and return books
        if self.status in ('borrowed','returned'):
            self.message_post(body=f'{self.env.user.name} is '
                                   f'{self.status} book. Date: {date.today()}')
            if self.status == 'borrowed':
                self.due_date = date.today() + timedelta(days=10)
                self.activity_schedule(
                    act_type_xmlid="mail.mail_activity_data_todo",
                    summary="Book Return Date Reminder",
                    note=(f"'{self.env.user.name}' borrowed "
                          f"{self.name} and return date is "
                          f"{self.due_date}."),
                    user_id=self.env.user.id,
                    date_deadline=self.due_date
                )
