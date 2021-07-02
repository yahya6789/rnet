from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sales_order_validation_cr = fields.Selection([
        ('none', 'None'),
        ('block', 'Block'),
        ('warning', 'Warning')
    ], 'Sales Order Validation', default='none',)

    delivery_order_validation_cr = fields.Selection([
        ('none', 'None'),
        ('block', 'Block'),
        ('warning', 'Warning')
    ], 'Delivery Order Validation', default='none',)

    maximum_allowed_ap_age = fields.Integer('Maximum Allowed AP Age')

    sales_order_validation_ow = fields.Selection([
        ('none', 'None'),
        ('block', 'Block'),
        ('warning', 'Warning')
    ], 'Sales Order Validation', default='none',)

    delivery_order_validation_ow = fields.Selection([
        ('none', 'None'),
        ('block', 'Block'),
        ('warning', 'Warning')
    ], 'Delivery Order Validation', default='none',)

