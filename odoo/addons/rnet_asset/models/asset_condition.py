from odoo import models, fields

class assetCondition(models.Model):
    _name = 'gut.asset.condition'

    name = fields.Char()