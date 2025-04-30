# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api


class SaleOrder(models.Model):
    """
    I inherited sale order for used to threshold functionality
    """
    _inherit = 'sale.order'

    approval_required = fields.Boolean(default=False)

    state = fields.Selection(
        selection=[
            ('draft', "Quotation"),
            ('sent', "Quotation Sent"),
            ('pending_approval', "Pending Approval"),
            ('sale', "Sales Order"),
            ('cancel', "Cancelled"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    def action_send_for_approval(self):
        """
        this method used for sending the email for approval to the sales manager.
        """
        self.state = 'pending_approval'
        sales_manager_approval_id = self.env['sales.manager.approval'].search(
            [('approval_threshold', '<=', self.amount_total)], order="approval_threshold desc", limit=1)
        self.message_post(body=f'sending email to the {sales_manager_approval_id.user_id.name} ')
        mail_template = self.env.ref(
            'moin_29042025.email_template_threshold_approval_required')
        mail_template.send_mail(sales_manager_approval_id.user_id.id, force_send=True)
        self.message_post(
            body=f'Approver is {sales_manager_approval_id.user_id.name}, Threshold amount is {sales_manager_approval_id.approval_threshold} and your sale order amount is {self.amount_total} ')

    def action_approve(self):
        """
        this method used for approve the sale order.
        """
        self.approval_required = False
        self.state = 'draft'
        self.message_post(body=f'{self.env.user.name} Approved on {datetime.now()} ')

    def action_approval_reminder_days(self):
        """
        this is scheduled actions for remaining approval.
        """
        pending_approvals = self.search([('approval_required','=',True)])
        for order in pending_approvals:
            sales_manager_approval_id = self.env['sales.manager.approval'].search(
                [('approval_threshold', '<=', order.amount_total)], order="approval_threshold desc", limit=1)
            mail_template = self.env.ref(
                'moin_29042025.email_template_threshold_approval_required')
            mail_template.send_mail(sales_manager_approval_id.user_id.id, force_send=True)
