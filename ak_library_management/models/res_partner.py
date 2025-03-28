# -*- coding: utf-8 -*-
from odoo import models, fields


class Partner(models.Model):
    """
    I inherited the res.user model and add the is_manger field.
    this field for user is manager or not.
    """
    _inherit = ["res.partner"]

    not_trust_worthy = fields.Boolean(string="Not Trust Worthy", default=False)
    is_member = fields.Boolean(string="Is Member", default=False)
