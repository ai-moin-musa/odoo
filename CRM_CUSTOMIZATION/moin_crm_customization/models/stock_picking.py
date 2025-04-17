# -*- coding: utf-8 -*-
from odoo import models, fields


class Picking(models.Model):
    """
    inherited stock.picking model for extend and added field job name.
    """
    _inherit = 'stock.picking'

    job_name = fields.Char(string="Job Name")
