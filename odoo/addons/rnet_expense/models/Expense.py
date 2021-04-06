from odoo import models, fields, api


class Sheet(models.Model):
    _inherit = 'hr.expense.sheet'
    seq = fields.Char(string='Expense Report No.', readonly=True, required=True, default='New')

    """
    Generate expense report no.
    """
    @api.model
    def create(self, vals):
        obj = super(Sheet, self).create(vals)
        if obj.seq == 'New':
            seq = self.env['ir.sequence'].next_by_code('expense.no') or 'New'
            obj.write({'seq': seq})
        return obj
