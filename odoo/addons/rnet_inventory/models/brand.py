from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class brand(models.Model):
    _name = 'gut.brand'
    _description = 'Product Brand'

    code = fields.Char('Brand Type', required=True)
    name = fields.Char('Brand', required=True)
    alias = fields.Char('Alias')
