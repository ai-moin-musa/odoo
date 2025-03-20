# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockWarehouse(models.Model):
    """
    I inherited stock.warehouse model and I added library_assistant_id which is many to one
    field and library_worker_ids which is many to many field for extending functionality of
    warehouse.
    """
    _inherit = "stock.warehouse"

    library_assistant_id = fields.Many2one(string="Library Assistant",comodel_name="hr.employee")
    library_worker_ids = fields.Many2many(string="Library Worker",comodel_name="hr.employee")

    @api.constrains('library_assistant_id', 'library_worker_ids')
    def _check_name_of_assistant_worker(self):
        """
        this method used for checking library assistant not assign in worker field.
        """
        if self.library_assistant_id in self.library_worker_ids:
            raise ValidationError(f'library assistant({self.library_assistant_id.name}) is not take as a library worker')
