from odoo import api, fields, models, _
from odoo.exceptions import UserError

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
            'context': {'current_id': self.id}
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
            'context': {'current_id': self.id}
        }

    def get_credit_so_warning_type(self):
        return str(
            self.env['ir.config_parameter'].sudo().get_param('rnet_credit_limit.sales_order_validation_cr') or 'block'
        )

    '''
    Fungsi cek credit limit dari addons.
    '''
    def is_credit_so_reached(self):
        partner = self.partner_id

        if partner.credit_limit > 0:
            if partner.credit > partner.credit_limit:
                return True
            else:
                credit = 0
                inv_total_amt = 0
                inv_rec = self.env['account.invoice'].search([
                    ('partner_id', '=', partner.id),
                    ('state', 'not in', ['draft', 'cancel'])
                ])

                sale_amount = self.search([
                    ('partner_id', '=', partner.id),
                ]).mapped('amount_total')

                sale_amt = sum([sale for sale in sale_amount])

                for inv in inv_rec:
                    inv_total_amt += inv.amount_total - inv.residual

                if partner.parent_id and partner.parent_id.credit < 0:
                    credit = partner.parent_id.credit

                elif partner.credit < 0:
                    credit = partner.credit

                total_sales = sale_amt + credit - inv_total_amt

                if total_sales > partner.credit_limit:
                    return True
                else:
                    return False
        else:
            return False

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
        if self.get_credit_so_warning_type() == 'none':
            self.confirm()

        if self.is_credit_so_reached() and (self.get_credit_so_warning_type() == 'block'):
            return self.show_block_window()

        if self.is_credit_so_reached() and (self.get_credit_so_warning_type() == 'warning'):
            return self.show_warning_message()
