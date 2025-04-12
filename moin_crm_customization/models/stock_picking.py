# -*- coding: utf-8 -*-
from odoo import models, fields


class Picking(models.Model):
    """
    inherited for extend and added field job name.
    """
    _inherit = 'stock.picking'

    job_name = fields.Char(related='move_ids.job_name', string="Job Name")
