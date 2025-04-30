# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class CustomController(http.Controller):

    @http.route('/save_review', type='http', auth='public', methods=['POST'], webiste=True, csrf=False)
    def save_review(self, **kwargs):
        """
        getting review and save review data into the database (create new review record)
        """
        product_review = request.env['product.review'].create({
            'product_id': kwargs.get('product_id'),
            'user_id': kwargs.get('user_id'),
            'rating': kwargs.get('rating'),
            'description': kwargs.get('review'),
        })
        return request.redirect('/shop')
