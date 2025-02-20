# -*- coding: utf-8 -*-
from odoo import models, fields


class ValidationWizard(models.TransientModel):
    """
    This model created for display the popup of
    validation wizard and added field message for
    validation error dynamic message
    """
    _name = "sale.order.validation.wizard"
    _description = "popup validation error"

    message = fields.Char(readonly=True)
