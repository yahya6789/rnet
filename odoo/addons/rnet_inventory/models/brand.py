from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class brand(models.Model):
    _name = 'gut.brand'
    _description = 'Product Brand'

    code = fields.Char('Brand Code', required=True)
    name = fields.Char('Brand Name', required=True)
    alias = fields.Char('Alias')
