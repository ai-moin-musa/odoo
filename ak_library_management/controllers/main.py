# -*- coding: utf-8 -*-
import base64
from odoo import http
from odoo.http import request
import zipfile
import io

class CustomController(http.Controller):
    @http.route('/contacts', type="http", auth="public", website=True)
    def display_contacts(self, **kwargs):
        """
        fetching all contacts and returning contact kanban view.
        :return: kanban view template with contacts data.
        """
        # Fetch contact records
        contacts = request.env['res.partner'].sudo().search([])
        # Render the template with data
        return request.render("ak_library_management.contacts_template", {'records': contacts})

    @http.route('/contacts/<model("res.partner"):partner>', type="http", auth="public", website=True)
    def display_contact_details(self, partner):
        """
        returning view for one contact which is user clicked on.
        :params: getting 'res.partner' record from the view
        :return: contact details view
        """
        return request.render('ak_library_management.contact_details_template', {
            'contact': partner
        })

    @http.route('/download_images', type='http', auth='public', methods=['POST'], webiste=True, csrf=False)
    def download_images(self, **kwargs):
        """
        fetch images of product from the product template and return zip file of images
        if product has multiple images either return single image
        """
        product_template_id = kwargs.get("product_template_id")
        product = request.env['product.template'].sudo().search([('id','=',product_template_id)])
        images = product.product_image_ids
        if images:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for image in images:
                    image_data = base64.b64decode(image.image_1920)
                    image_filename = f"{product.name}_{image.id}"
                    zip_file.writestr(image_filename, image_data)
                image_data = base64.b64decode(product.image_1920)
                image_filename = f"{product.name}_{product.id}"
                zip_file.writestr(image_filename, image_data)
            zip_buffer.seek(0)
            return request.make_response(zip_buffer.getvalue(), headers=[
                ('Content-Type', 'application/zip'),
                ('Content-Disposition', f'attachment; filename="{product.name}_images.zip"')
            ])
        else:
            image_data = product.image_1920
            if image_data:
                image_data = base64.b64decode(image_data)
                filename = f"image_{product.name}"
                return request.make_response(image_data, headers=[
                    ('Content-Type', 'image/jpeg'),
                    ('Content-Disposition', f'attachment; filename="{filename}"')
                ])

    @http.route('/customer', type='http', auth='public', website=True)
    def customer_detail(self, **kwargs):
        """
        returning customer detail template which is used for getting specific customer
        data in the same page of form, both html form and data container in this template.
        """
        return request.render('ak_library_management.customer_page_view_template')

    @http.route('/customer/fetch-customer', type='json', auth='public', csrf=False)
    def fetch_customer_detail(self, email):
        """
        this method return data of customer based on the entered email.
        :params: email.
        :return: returning dictionary (Json Formatted) data of customer.
        """
        partner = request.env['res.partner'].sudo().search([('email', '=', email)],limit=1)
        return {
            'name' : partner.name,
            'company' : partner.company_id.name or "customer does not have any company.",
            'phone' : partner.phone or "customer does not have any contact number.",
            'vat' : partner.vat or "customer does not have Tax ID.",
            'found': not partner,
        }
