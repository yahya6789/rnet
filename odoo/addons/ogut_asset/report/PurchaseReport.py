from odoo import models, api, fields


class PurchaseReport(models.Model):
    _inherit = 'purchase.report'

    project_name = fields.Char('Job Order No.')
