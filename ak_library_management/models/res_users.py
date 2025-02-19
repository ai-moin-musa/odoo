from odoo import models, fields


class ResUsers(models.Model):
    _inherit = ["res.users"]

    is_manager = fields.Boolean(string="Is Manager")
