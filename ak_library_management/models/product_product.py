# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'
    vendor_ids = fields.One2many(comodel_name='product.supplierinfo', inverse_name='product_id', string='Vendor on Variants')
