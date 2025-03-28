# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    price_unit = fields.Monetary(
        string='Unit Price',
        compute="_compute_price_unit", store=True, readonly=False, precompute=True
    )