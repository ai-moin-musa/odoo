from odoo import http
from odoo.http import request


class ContactsController(http.Controller):
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
