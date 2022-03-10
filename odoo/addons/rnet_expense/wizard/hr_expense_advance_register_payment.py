from odoo import models, fields, api


class HrExpenseAdvanceRegisterPaymentWizard(models.TransientModel):
    _inherit = 'hr.expense.advance.register.payment.wizard'

    transfer_to = fields.Many2one('account.journal', string='Transfer To',
                                  domain="['|',('type', '=', 'bank'), ('type', '=', 'cash')]")
    hide_transfer_to = fields.Boolean(compute='_compute_hide_transfer_to', default=True)

    @api.depends('transfer_to')
    def _compute_hide_transfer_to(self):
        context = dict(self._context or {})
        transaction_type = context.get('transaction_type', None)
        if transaction_type == 'petty_cash':
            self.hide_transfer_to = False
        else:
            self.hide_transfer_to = True
