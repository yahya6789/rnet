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
            for exp in obj.expense_line_ids:
                exp.update_seq_no(seq)
        return obj


class Expense(models.Model):
    _inherit = 'hr.expense'
    seq = fields.Char(string='Expense Report No.', required=True, default='New')

    def update_seq_no(self, seq):
        self.seq = seq
        return
