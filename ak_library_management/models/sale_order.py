# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    """"
    I inherited sale.order model and added fields,
    permission_manager field which is use for is needed
    permission of manager, approved field which is use for
    manager approved the current sale order, is_manager field
    which is use for checking the current user is manger or not
    """
    _inherit = ['sale.order']

    permission_manager = fields.Boolean(default=False)
    approved = fields.Boolean(string="Approved Status", default=False)
    is_manager = fields.Boolean(compute="_get_is_manager")

    def action_confirm(self):
        """
        Confirm the given quotation(s) and set their confirmation date.
        If the corresponding setting is enabled, also locks the Sale Order.
        Override Method
        :return: True or popup wizard
        :rtype: bool
        :raise: UserError if trying to confirm cancelled SO's
        """
        low_quant_product = []
        if not self.approved:
            low_quant_product = [rec.product_id.name for rec in self.order_line
                                 if rec.product_id.qty_available < 5]
        if len(low_quant_product) > 0:
            self.permission_manager = True
            self.approved = False
            return {
                'type': 'ir.actions.act_window',
                'name': "Validation Error",
                'res_model': 'sale.order.validation.wizard',
                'target': 'new',
                'view_mode': 'form',
                'context': {
                    'default_message':
                        f"Approval needed! "
                        f"The following products have low stock: "
                        f"({','.join(prod_name for prod_name in low_quant_product)})"},
            }
        return super().action_confirm()

    def approve(self):
        """
        this method is approved the sale order of user.
        """
        if self.env.user.is_manager:
            self.permission_manager = False
            self.approved = True

    def reject(self):
        """
        this method reject the sale order and canceled the sale order.
        """
        self.permission_manager = False
        return super().action_cancel()

    @api.depends()
    def _get_is_manager(self):
        """
        this compute method for getting current user
        is_manger field boolean value (True/False)
        """
        self.is_manager = self.env.user.is_manager
