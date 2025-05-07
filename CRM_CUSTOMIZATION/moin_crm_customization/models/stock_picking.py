# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Picking(models.Model):
    """
    inherited stock.picking model for extend and added field job name.
    """
    _inherit = 'stock.picking'

    job_name = fields.Char(string="Job Name", compute="_compute_job_name_from_sale_order", store=True)

    @api.depends('sale_id.job_name')
    def _compute_job_name_from_sale_order(self):
        for rec in self:
            if rec.sale_id.job_name:
                rec.job_name = rec.sale_id.job_name
            if rec.project_id:
                rec.project_id.name = f"{rec.sale_id.name} - {rec.job_name}"
                rec.project_id.job_name = rec.job_name
