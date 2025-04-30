# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    """
    inherited sale order line and override methods for used functionality to threshold
    """
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        """
        I override this method for approval needed when amount is greate than thresholds
        """
        res = super().create(vals_list)
        for record in res:
            id_and_thresholds = self.env['sales.manager.approval'].search_read([], fields=['id', 'approval_threshold'])
            thresholds_amount = [i.get('approval_threshold') for i in id_and_thresholds]
            print(record.order_id.amount_total)
            if record.order_id.amount_total > min(thresholds_amount):
                record.order_id.approval_required = True
            else:
                record.order_id.approval_required = False
        return res
