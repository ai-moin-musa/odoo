# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    """
    inherited sale order and added job name field.
    """
    _inherit = 'sale.order'

    job_name = fields.Char(string="Job Name")
