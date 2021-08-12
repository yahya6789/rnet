from odoo import models, fields

class assetStatus(models.Model):
    _name = 'gut.asset.status'

    name = fields.Char()