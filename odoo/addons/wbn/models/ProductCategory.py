from odoo import models, api, fields

import logging
_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = "product.category"

    internal_reference = fields.Char('Internal Reference')
