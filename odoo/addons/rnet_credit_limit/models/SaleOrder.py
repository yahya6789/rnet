from odoo import api, fields, models, _
from odoo.exceptions import UserError
from .CreditLimit import CreditLimit

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def show_warning_message(self):
        message_id = self.env['message.wizard'].create({'message': "This customer has reached his credit limit, "
                                                                   "do you want to continue?"})
        return {
            'name': 'Warning',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'res_id': message_id.id,
            'target': 'new',
            'context': {'current_id': self.id, 'current_model': 'sale.order'}
        }

    def show_block_window(self):
        view_id = self.env.ref('customer_credit_management.credit_management_limit_wizard').id
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.customer.credit.limit.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'name': 'Customer Credit Limit',
            'views': [[view_id, 'form']],
            'context': {'current_id': self.id, 'current_model': 'sale.order'}
        }

    def get_credit_so_warning_type(self):
        return str(
            self.env['ir.config_parameter'].sudo().get_param('rnet_credit_limit.sales_order_validation_cr') or 'block'
        )

    '''
    Fungsi action_confirm-nya modul sales
    '''
    @api.multi
    def confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'confirmation_date': fields.Datetime.now()
        })

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
            self.action_done()
        return True

    @api.multi
    def action_confirm(self):
        partner = self.partner_id

        if self.get_credit_so_warning_type() == 'none':
            self.confirm()

        inv_rec = self.env['account.invoice'].search([
            ('partner_id', '=', partner.id),
            ('state', 'not in', ['draft', 'cancel'])
        ])

        sale_amount = self.search([
            ('partner_id', '=', partner.id),
        ]).mapped('amount_total')

        cr = CreditLimit()
        is_credit_so_reached = cr.is_credit_so_reached(self.partner_id, inv_rec, sale_amount)

        if is_credit_so_reached and (self.get_credit_so_warning_type() == 'block'):
            return self.show_block_window()

        if is_credit_so_reached and (self.get_credit_so_warning_type() == 'warning'):
            return self.show_warning_message()
