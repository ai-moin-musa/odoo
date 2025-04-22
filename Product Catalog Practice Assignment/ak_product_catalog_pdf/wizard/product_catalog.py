# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError


class ProductCatalog(models.TransientModel):
    """
    Product Catalog model is containing information of
    products for generating product catalog.
    """
    _name = "product.catalog"
    _description = "Product Catalog"

    catalog_style = fields.Selection(
        selection=[('style1', 'Style 1'), ('style2', 'Style 2')],
        string="Catalog Style",
        default="style1",
    )
    page_break_after = fields.Integer(string="Page Break After", default=1)
    product_ids = fields.Many2many(comodel_name='product.product', string="Products")

    def action_print_pdf(self):
        """
        this method used for print pdf report of products catalog.
        raise validation error if page break after value is zero
        or less than zero.
        :return: action according the condition ('there are two actions one for style 1
                                                    and second one for style 2')
        """
        self.ensure_one()
        if self.page_break_after <= 0:
            raise ValidationError("A page break after value can not be zero or less than zero")
        if self.catalog_style == "style2":
            return self.env.ref('ak_product_catalog_pdf.action_report_product_catalog_style_two').report_action(self)
        return self.env.ref('ak_product_catalog_pdf.action_report_product_catalog_style_one').report_action(self)
