from odoo import models, fields, api, _


class PurchaseLineHistory(models.Model):
    _name = 'purchase.order.line.history'
    _inherit = 'purchase.order.line'

    order_id = fields.Many2one('purchase.order.history', string='Order Reference', index=True, required=True,
                               ondelete='cascade')
