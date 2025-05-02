# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteCustomController(WebsiteSale):

    def sitemap_products(env, rule, qs):
        return super().sitemap_products()

    @http.route('/shop/<model("product.template"):product>/', type='http', auth='public', website=True,
                sitemap=sitemap_products, readonly=True)
    def product(self, product, category='', search='', **kwargs):
        """
        Show custom out-of-stock page or standard product page.
        """
        if not request.website.has_ecommerce_access():
            return request.redirect('/web/login')

        if product.is_out_of_stock:
            return request.render('custom_out_of_stock_page.custom_out_of_stock_template', {
                'products': product
            })
        return super().product(product, category=category, search=search, **kwargs)
