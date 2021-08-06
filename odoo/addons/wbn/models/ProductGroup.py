from odoo import models, api, fields


class ProductGroup(models.Model):
    _name = "product.group"

    _sql_constraints = [('code_uniq', 'unique (code)', "Product group code must be unique!"),]

    code = fields.Char('Code', required=True)
    name = fields.Char('Name')
    description = fields.Char('Description')
