from odoo import models, fields, api, _
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    po_generate_multiple_asset = fields.Boolean('PO Generate Multiple Asset')
    product_prefix = fields.Char("Product Prefix")


class Product(models.Model):
    _inherit = 'product.product'

    # categ_id
    is_generate_multiple_asset = fields.Boolean(compute='_is_generate_multiple_asset',
                                                string='Is Generate Multiple Asset')

    @api.one
    def _is_generate_multiple_asset(self):
        self.is_generate_multiple_asset = self.categ_id.po_generate_multiple_asset


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand = fields.Many2one('gut.brand', 'Brand')
    brand_type = fields.Char('Brand Type')
    display_as_delivery_cost = fields.Boolean(default=False)
