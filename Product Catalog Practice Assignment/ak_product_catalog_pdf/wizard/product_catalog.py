# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductCatalog(models.TransientModel):

    _name = "product.catalog"
    _description = "Product Catalog"

    catalog_style = fields.Selection(
        selection=[('style1','Style 1'),('style2','Style 2')],
        string="Catalog Style",
    )
    page_break_after = fields.Integer(string="Page Break After")
    product_ids = fields.Many2many(comodel_name='product.product', string="Products")

    def action_confirm(self):
        print(self)
        for rec in self:
            print(rec)