# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    """
    I inherited the res.config.settings model and add the borrow_limit field for
    extending setting library management application.
    """
    _inherit = "res.config.settings"

    borrow_limit = fields.Integer(
        string="Borrowing limit",
        config_parameter="ak_library_management.borrow_limit"
    )
