# -*- coding: utf-8 -*-
from odoo import models,fields


class Partner(models.Model):
    _inherit = ["res.partner"]

    not_trust_worthy = fields.Boolean(string="Not Trust Worthy",default=False)
    is_member = fields.Boolean(string="Is Member",default=False)