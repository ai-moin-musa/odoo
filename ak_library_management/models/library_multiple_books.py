# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LibraryMultipleBooks(models.TransientModel):
    """
    This model for generating the bulk record of books.
    This model Contains books names, author_id which is Many to one
    from the res.partner model, category_id which is Many to one field
    from the library.book.category model, price of the book, bulk_books_count
    is contain number of books created by this model
    """
    _name = "library.multiple.books"
    _description = "Library Multiple Books"
    _rec_name = "book_names"

    book_names = fields.Text(string="Book Names")
    author_id = fields.Many2one("res.partner", "Author")
    category_ids = fields.Many2one(
        "library.book.category", "Books category",
        default=lambda self: self.env['library.book.category']
        .search([], limit=1).id)
    price = fields.Integer(string="price")
    bulk_books_count = fields.Integer(string="Product Count",
                                      compute="_compute_bulk_books_count")
    product_ids = fields.Many2many(comodel_name="product.template")

    def action_create_products(self):
        """
        This Method used to create multiple products
        and also send notification to user for created
        products.
        :params: None
        :return: None
        :rtype: None
        """
        for book_name in self.book_names.split(','):
            book_name.strip()
            if not self.env['product.template'].search([('name', '=', book_name)]):
                products = self.env['product.template'].create({
                    'name': book_name,
                    'author': self.author_id.name
                })
                self.product_ids = [(4, products.id)]
                # send the notification to the current user for created message
                self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                    'type': 'success',
                    'message': f"{book_name} is created as product.",
                })
            else:
                recs = self.env['product.template'].search([('name', '=', book_name)])
                for rec in recs:
                    self.product_ids = [(4, rec.id)]

    def action_revert_changes(self):
        """
        This function revert changes
        If clicked, it will delete all products created
        from the current Bulk Upload Books Record session.
        """
        self.product_ids.unlink()

    @api.depends("product_ids")
    def _compute_bulk_books_count(self):
        """
        This function compute based on the product_ids field.
        count the all books or products in the current bulk
        """
        for record in self:
            record.bulk_books_count = len(record.product_ids) if record.product_ids else 0

    def bulk_books(self):
        """
        This function redirect to the product list view.
        :return: this method returning action
        :rtype: dict
        """
        action = {
            'name': 'Bulk Books',
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'list,form' if len(self.product_ids) > 1 else 'form',
            'domain': [("id", "in", self.product_ids.ids)],
        }
        if len(self.product_ids) == 1:
            action['res_id'] = self.product_ids.id
        return action
