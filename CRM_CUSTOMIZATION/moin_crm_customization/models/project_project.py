# -*- coding: utf-8 -*-
from odoo import models, fields


class Project(models.Model):
    """
    inherited for extend module added job name field.
    """
    _inherit = 'project.project'

    job_name = fields.Char(string="Job Name")
