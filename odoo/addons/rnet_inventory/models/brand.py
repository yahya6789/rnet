from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class Brand(models.Model):
    _name = 'gut.brand'
    _description = 'Product Brand'

    _sql_constraints = [('code_name', 'unique (name)', "Brand name must be unique!"), ]

    code = fields.Char('Brand Code', required=True)
    name = fields.Char('Brand Name', required=True)
    alias = fields.Char('Alias')

    product_count = fields.Integer(string='Product Count', compute='_get_product_count')

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
    def _get_product_count(self):
        res = self.env['product.template'].search_count([('brand', '=', self.id)])
        self.product_count = res or 0
