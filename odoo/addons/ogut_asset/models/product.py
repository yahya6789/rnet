from odoo import models, fields, api, _
from datetime import date
import logging
_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = 'product.category'

    po_generate_multiple_asset = fields.Boolean('PO Generate Multiple Asset')

class Product(models.Model):
    _inherit = 'product.product'

    #categ_id
    is_generate_multiple_asset = fields.Boolean(compute='_is_generate_multiple_asset', string='Is Generate Multiple Asset')

    @api.one
    def _is_generate_multiple_asset(self):
        self.is_generate_multiple_asset = self.categ_id.po_generate_multiple_asset

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand = fields.Char('Brand')