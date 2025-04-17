# -*- coding: utf-8 -*-
from odoo import models, fields


class StockMove(models.Model):
    """
    inherited stock.move and override the two methods and
    added field job name
    """
    _inherit = 'stock.move'

    job_name = fields.Char(string="Job Name")

    def _prepare_procurement_values(self):
        """
        override this method for passing job name value to the manufacturing orders.
        """
        vals = super()._prepare_procurement_values()
        vals["job_name"] = self.group_id.sale_id.job_name
        return vals

    def _get_new_picking_values(self):
        """Inherit method for pass value from sale order to delivery order."""
        res = super()._get_new_picking_values()
        res["job_name"] = self.group_id.sale_id.job_name
        return res
