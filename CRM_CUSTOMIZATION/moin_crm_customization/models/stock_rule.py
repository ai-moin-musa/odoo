# -*- coding: utf-8 -*-
from odoo import models, fields


class StockRule(models.Model):
    """
    inherited stock.rule model for override methods and passing value of job name to the
    delivery order and manufacturing orders.
    """
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom,
                               location_dest_id, name, origin, company_id, values):
        """
        override this method for passing job name value to the stock.move for delivery orders
        """
        res = super()._get_stock_move_values(product_id, product_qty, product_uom,
                                             location_dest_id, name, origin, company_id, values)
        res['job_name'] = values.get('job_name', False)
        return res

    def _prepare_mo_vals(
            self,
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
    ):
        """
        Method for passing value from sale order to manufacturing order.
        """
        vals = super(StockRule, self)._prepare_mo_vals(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
        )
        vals["job_name"] = values.get("job_name")
        return vals
