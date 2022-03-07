from odoo import models, fields, api
from odoo.exceptions import ValidationError


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


class ExpenseAdvance(models.Model):
    _inherit = 'hr.expense.advance'

    transaction_type = fields.Selection([('petty_cash', 'Petty Cash'), ('hutang_usaha', 'Hutang Usaha'), ],
                                        'Transaction Type', default='petty_cash')

    # Cek account petty cash employee ybs.
    def _validate_pettycash(self, values):
        if values.get('transaction_type'):
            if not self.employee_id.user_id.partner_id.account_pettycash_id:
                raise ValidationError('Untuk tipe transaksi petty cash, Account Pettycash employee harus dipilih')

    @api.model
    def create(self, values):
        self._validate_pettycash(values)
        return super(ExpenseAdvance, self).create(values)

    @api.multi
    def write(self, values):
        self._validate_pettycash(values)
        return super(ExpenseAdvance, self).write(values)
