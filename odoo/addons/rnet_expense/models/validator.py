from odoo.exceptions import ValidationError

class ExpenseValidator:
    def validate_pettycash(self, values):
        if values.get('transaction_type') == 'petty_cash' and values.get('account_pettycash_id') is False:
            raise ValidationError('Untuk tipe transaksi petty cash, Account Pettycash employee harus dipilih')
