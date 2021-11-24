from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class Brand(models.Model):
    _name = 'gut.brand'
    _description = 'Product Brand'

    code = fields.Char('Brand Type', required=True)
    name = fields.Char('Brand', required=True)
    alias = fields.Char('Alias')

    product_count = fields.Integer(string='Product Count', compute='_gut_product_count')

    @api.multi
    def open_products(self):
        for brand in self:
            return {
                'name': 'Products',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'product.template',
                'type': 'ir.actions.act_window',
                'domain': [('brand', '=', brand.id)],
            }
        pass

    @api.multi
    def _gut_product_count(self):
        res = self.env['product.template'].search_count([('brand', '=', self.id)])
        self.product_count = res or 0
