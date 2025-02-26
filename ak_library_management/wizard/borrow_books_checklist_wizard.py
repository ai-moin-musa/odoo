# -*- coding: utf-8 -*-
from odoo import models, fields


class BorrowBooksChecklistWizard(models.TransientModel):
    _name = "borrow.books.checklist.wizard"
    _description = "Borrow Books Checklist Wizard"

    message = fields.Char(readonly=True)

    def action_cancel(self):
        """
        this method for cancel button when clicked on cancel button
        record deleted in the borrow_transaction_history table
        """
        rec = self.env.context.get('active_id')
        self.env["borrow.transaction.history"].browse(rec).unlink()
