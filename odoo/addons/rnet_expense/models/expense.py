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

    @api.model
    def create(self, values):
        employee_id = self.env['hr.employee'].search([('id', '=',  values.get('employee_id'))])
        partner_id = employee_id.address_home_id
        if values.get('transaction_type') == 'petty_cash' and partner_id.account_pettycash_id.id is False:
            raise ValidationError('Untuk tipe transaksi petty cash, Account Pettycash employee harus dipilih')
        return super(ExpenseAdvance, self).create(values)

    @api.multi
    def write(self, values):
        transaction_type_changed = values.get('transaction_type')
        partner_id = self.employee_id.address_home_id

        if transaction_type_changed is not None:
            # field transaction_type berubah
            transaction_type = values.get('transaction_type')
        else:
            transaction_type = self.transaction_type

        if transaction_type == 'petty_cash' and partner_id.account_pettycash_id.id is False:
            raise ValidationError('Untuk tipe transaksi petty cash, Account Pettycash employee harus dipilih')

        return super(ExpenseAdvance, self).write(values)
