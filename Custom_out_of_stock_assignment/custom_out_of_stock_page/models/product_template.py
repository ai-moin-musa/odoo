# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    """
    inherited the product template class and extend with is_out_of_stock field.
    """
    _inherit = "product.template"

    is_out_of_stock = fields.Boolean(string="Not Available")
    out_of_stock_message = fields.Html(string="Custom Out-of-Stock Message")
