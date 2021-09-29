from odoo import models, fields, api, _


class PurchaseOrderHistory(models.Model):
    _name = 'purchase.order.history'
    _inherit = 'purchase.order'

    original_id = fields.Integer(required=True)
    revision = fields.Integer(default=0)
    revision_date = fields.Datetime()


