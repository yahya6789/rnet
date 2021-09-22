from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def create(self, vals_list):
        template = super(ProductTemplate, self).create(vals_list)
        ir = template.default_code
        if not ir:
            template.default_code = self._get_product_prefix(template.categ_id.id)
        return template

    def _get_product_prefix(self, categ_id):
        categ = self.env['product.category'].search([
            ('id', '=', categ_id)
        ])
        prefix = categ.product_prefix
        if not prefix:
            return None
        seq = self.env['ir.sequence'].next_by_code('product.seq') or None
        if not seq:
            raise UserError(_("Sequence is null or not found"))
        return prefix + str(seq)
