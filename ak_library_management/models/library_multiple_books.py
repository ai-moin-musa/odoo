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

    book_names = fields.Text(string="Book Names")
    author_id = fields.Many2one("res.partner", "Author")
    category_ids = fields.Many2one(
        "library.book.category", "Books category",
        default=lambda self: self.env['library.book.category']
        .search([], limit=1).id)
    price = fields.Integer(string="price")
    bulk_books_count = fields.Integer(string="Product Count",
                                      compute="_compute_bulk_books_count")

    def create_products(self):
        """
        This function create multiple books in product.template model.
        which is comma separated books names given input by user.
        """
        for book_name in self.book_names.split(','):
            # removing spaces in to the book name
            book_name = book_name.strip()
            if not bool(self.env['product.template'].search([('name', '=', book_name)])):
                self.env['product.template'].create({
                    'name': book_name,
                    'author': self.author_id.name
                })

    def revert_changes(self):
        """
        This function revert changes
        If clicked, it will delete all products created
        from the current Bulk Upload Books Record session.
        """
        book_names_list = self.book_names.split(',')
        self.env['product.template'].search([('name', '=', book_names_list)]).unlink()

    @api.depends("book_names")
    def _compute_bulk_books_count(self):
        """
        This function compute based on the book_names field.
        count the all books or products in the current bulk
        """
        if self.book_names:
            book_names_list = self.book_names.split(',')
            self.bulk_books_count = (self.env['product.template'].
                                     search_count([("name", "in", book_names_list)]))
        else:
            self.bulk_books_count = 0

    def bulk_books(self):
        """
        This function redirect to the product list view.
        """
        book_names_list = self.book_names.split(',')
        product_rec = self.env['product.template'].search([("name","in",book_names_list)])
        return {
            'name': 'Bulk Books',
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'list,form' if len(book_names_list) > 1 else 'form',
            'domain': [("name", "in", book_names_list)] if len(book_names_list) else [],
            'res_id': product_rec[0].id if len(product_rec) == 1 else None,
        }
