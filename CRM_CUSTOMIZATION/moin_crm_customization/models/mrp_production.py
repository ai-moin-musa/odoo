# -*- coding: utf-8 -*-
from odoo import models, fields


class MrpProduction(models.Model):
    """
    inherited mrp production and added job name field.
    """
    _inherit = 'mrp.production'

    job_name = fields.Char(string="Job Name")
