# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountMove(models.Model):
    """
    Inherited account.move model and added field job_name
    """
    _inherit = "account.move"

    job_name = fields.Char(string="job_name")
