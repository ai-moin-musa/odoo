# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    """
    inherited sale order and added job name field.
    """
    _inherit = 'sale.order'

    job_name = fields.Char(string="Job Name", compute="_compute_job_name_from_opportunity_crm", store=True)

    def _prepare_invoice(self):
        """
        override this method for used to passing value of job name
        """
        vals = super()._prepare_invoice()
        vals['job_name'] = self.job_name
        return vals

    @api.depends('opportunity_id', 'opportunity_id.name')
    def _compute_job_name_from_opportunity_crm(self):
        """
        this method used for whenever changes the opportunity id or opportunity's name
        so store the job name same as opportunity name.
        """
        for rec in self:
            if rec.opportunity_id:
                rec.job_name = rec.opportunity_id.name
