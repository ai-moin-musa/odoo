from itertools import product

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            for key, value in val.items():
                print("---------------------Single----REC---------------------")
                print("---------------------Key------------------------")
                print(key)
                print("---------------------Value-----------------------")
                print(value)
                print("---------------------END-----------REC-----------------")
                if key == "order_line":
                    print("===============Order=====Line================")
                    for i in val[key]:
                        print("=============OL==============")
                        print(i)
                        print("==========OL===========")
        rec = super().create(vals_list)
        print(rec)
        return rec

    def action_confirm(self):
        """
        Confirm the given quotation(s) and set their confirmation date.
        If the corresponding setting is enabled, also locks the Sale Order.
        Override Method
        :return: True
        :rtype: bool
        :raise: UserError if trying to confirm cancelled SO's
        """
        low_quant_product = [product_id.name for product_id in self.order_line
                             if product_id.product_uom_qty < 5]
        if len(low_quant_product) > 0:
            raise ValidationError(f"Approval needed! The following books have low stock: ({','.join(prod_name for prod_name in low_quant_product)})")
        return super().action_confirm()
