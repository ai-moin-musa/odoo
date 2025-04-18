# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models, fields
from pkg_resources import require


class ProductCatalog(models.TransientModel):

    _name = "product.catalog"
    _description = "Product Catalog"

    catalog_style = fields.Selection(
        selection=[('style1','Style 1'),('style2','Style 2')],
        string="Catalog Style",
        default="style1",
    )
    def _default_product_id(self):
        return self.env['product.product'].search([('id','in',[15,16,23,36,18,19,20,21])])

    page_break_after = fields.Integer(string="Page Break After",default=1)
    product_ids = fields.Many2many(comodel_name='product.product', string="Products", default=lambda self: self._default_product_id())

    def action_print_pdf(self):
        self.ensure_one()
        print(self)
        return self.env.ref('ak_product_catalog_pdf.action_report_product_catalog_style_one').report_action(self)