# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    """
    inherited sale order line and override methods for delivery customization
    """
    _inherit = 'sale.order.line'

    def _prepare_procurement_values(self, group_id):
        """
        override and update the values dictionary with job name.
        """
        values = super()._prepare_procurement_values(group_id)
        values['job_name'] = self.order_id.job_name
        return values

    def _timesheet_create_project_prepare_values(self):
        """ inherit method for passing value from sale order to project"""
        values = super()._timesheet_create_project_prepare_values()
        values['name'] = '%s - %s' % (
            self.order_id.name, self.order_id.job_name) if self.order_id.job_name else self.order_id.name
        values["job_name"] = self.order_id.job_name
        return values
