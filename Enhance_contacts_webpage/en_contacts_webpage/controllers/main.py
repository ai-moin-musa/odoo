# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


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
        return request.render("en_contacts_webpage.contacts_template", {'records': contacts})

    @http.route('/contacts/<model("res.partner"):partner>', type="http", auth="public", website=True)
    def display_contact_details(self, partner):
        """
        returning view for one contact which is user clicked on.
        :params: getting 'res.partner' record from the view
        :return: contact details view
        """
        return request.render('en_contacts_webpage.contact_details_template', {
            'contact': partner
        })

    @http.route('/save_contact', type='json', auth='user', website=True, csrf=False)
    def save_contact(self, contact_id, email, phone, name, website, address):
        """
        save updated contact details and return status and message
        :params: contact_id, email, phone, name, website, address
        :return: status and message
        """
        try:
            partner = request.env['res.partner'].sudo().browse(int(contact_id))
            if request.env['res.partner'].search(
                [('id', '!=',contact_id), ('email', '=', email)]):
                raise ValidationError('this email already taken. please take other email address.')

            if partner.exists():
                partner.write({
                    'email': email,
                    'phone': phone,
                    'name': name,
                    'website': website,
                    'contact_address_inline': address,
                })
                return {'status': 'success', 'message': 'Contact updated successfully.'}
            else:
                return {'status': 'error', 'message': 'Partner not found.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}