# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    """
    I inherited the res.config.settings model and add the sales_manager_approval_ids many2many field for
    extending general setting of the application.
    """
    _inherit = "res.config.settings"

    sales_manager_approval_ids = fields.Many2many(comodel_name="sales.manager.approval",string="Sales Manager Approvals")
