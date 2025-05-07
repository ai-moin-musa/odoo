# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpProduction(models.Model):
    """
    inherited mrp production and added job name field.
    """
    _inherit = 'mrp.production'

    job_name = fields.Char(compute="_compute_job_name_from_sale_order", string='Job Name', store=True)

    @api.depends("procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id.job_name",
                 "sale_line_id.order_id.job_name")
    def _compute_job_name_from_sale_order(self):
        for production in self:
            if production.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id.job_name:
                production.job_name = production.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id.job_name
