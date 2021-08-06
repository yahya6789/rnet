from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_group = fields.Many2one('product.group', string='Product Group')
