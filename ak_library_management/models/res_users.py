# -*- coding: utf-8 -*-
from odoo import models, fields


class ResUsers(models.Model):
    """
    I inherited the res.user model and add the is_manger field.
    this field for user is manager or not.
    """
    _inherit = ["res.users"]

    is_manager = fields.Boolean(string="Is Manager")
