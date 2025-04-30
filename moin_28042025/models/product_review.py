# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductReview(models.Model):
    """
    this class used for storing the review details of the product.
    """
    _name = "product.review"
    _description = "Product Review"

    product_id = fields.Many2one(comodel_name="product.template", required=True)
    user_id = fields.Many2one(comodel_name="res.users", string="Reviewer")
    rating = fields.Selection(
        selection=[
            ('1', '1 Star'),
            ('2', '2 Star'),
            ('3', '3 Star'),
            ('4', '4 Star'),
            ('5', '5 Star'),
        ],
        string="Rating")
    description = fields.Text(string="Review")
    create_date = fields.Datetime(string='Create Date', default=lambda self: fields.Datetime.now())
