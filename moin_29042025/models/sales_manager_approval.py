# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SalesManagerApproval(models.Model):
    """
    this model used for user can configure multiple approval threshold records in this model.
    """
    _name = "sales.manager.approval"
    _description = "Sales Manager Approval"

    def _default_currency_id(self):
        """
        this method set default currency according to the user's company currency
        """
        return self.env.user.company_id.currency_id

    user_id = fields.Many2one(comodel_name='res.users', string="Sales Manager")
    approval_threshold = fields.Integer(string="Approval Threshold Amount")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self._default_currency_id())
    @api.model_create_multi
    def create(self, vals_list):
        """
        I override this method for restricting the duplicate thresholds (prevent duplicate records)
        """
        print(vals_list)
        for val in vals_list:
            if self.search([('user_id','=',val.get('user_id')),('approval_threshold','=',val.get('approval_threshold'))]).exists():
                raise ValidationError('Threshold amount is already configured.')
        res = super().create(vals_list)
        return res
