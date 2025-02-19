# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
    price = fields.Integer(string="price", default=0)
    bulk_books_count = fields.Integer(string="Product Count",
                                      compute="_compute_bulk_books_count")

    def create_products(self):
        """
        This function create multiple books in product.template model.
        which is comma separated books names given input by user.
        """
        # this is condition for user can not give empty book names
        if not self.book_names or ",," in self.book_names:
            # Raising Validation Error if book names are not valid
            raise ValidationError("Invalid Book Names")
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
        for book_name in self.book_names.split(','):
            book_name = book_name.strip()
            self.env['product.template'].search([('name', '=', book_name)]).unlink()
        # so set created value is 0

    @api.depends("book_names")
    def _compute_bulk_books_count(self):
        """
        This function compute based on the book_names field.
        count the all books or products in the current bulk
        """
        if self.book_names:
            book_names_list = [book_name.strip() for book_name in self.book_names.split(",")]
            self.bulk_books_count = (self.env['product.template'].
                                     search_count([("name", "in", book_names_list)]))
        else:
            self.bulk_books_count = 0  # if book_names has not any value so set count to zeros

    def bulk_books(self):
        """
        This function redirect to the product list view.
        """
        book_names_list = [book_name.strip() for book_name in self.book_names.split(",")]
        if len(book_names_list) == 1:
            product_id = self.env['product.template'].search([("name", "=", book_names_list[0])])
            return {
                'name': 'Bulk Books',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'product.template',
                'res_id': product_id.id,
            }
        return {
            'name': 'Bulk Books',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'product.template',
            'domain': [("name", "in", book_names_list)],
        }
