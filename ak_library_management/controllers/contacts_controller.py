from odoo import http
from odoo.http import request


class ContactsController(http.Controller):
    @http.route(['/contacts'], type="http", auth="public", website=True)
    def display_contacts(self, **kwargs):
        # Fetch contact records
        contacts = request.env['res.partner'].sudo().search([])
        # Prepare data for the template
        values = {
            'records': contacts
        }
        # Render the template with data
        return request.render("ak_library_management.contacts_template", values)

    @http.route(['/contacts/<model("res.partner"):partner>'], type="http", auth="public", website=True)
    def display_contact_details(self, **kwargs):
        return request.render('ak_library_management.contact_details_template', {
            'contact': kwargs.get("partner")
        })
