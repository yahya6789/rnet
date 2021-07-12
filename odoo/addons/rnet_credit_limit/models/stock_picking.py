from odoo import models, _, fields, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from .credit_limit import CreditLimit

import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def show_warning_message(self):
        message_id = self.env['delivery.credit.limit.warning'].create({
            'message': "This customer has reached his credit limit, do you want to continue?"
        })

        return {
            'name': 'Warning',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'delivery.credit.limit.warning',
            'res_id': message_id.id,
            'target': 'new',
            'context': {'current_id': self.id}
        }

    def get_credit_do_warning_type(self):
        return str(
            self.env['ir.config_parameter'].sudo().get_param(
                'rnet_credit_limit.delivery_order_validation_cr') or 'block'
        )

    @api.multi
    def validate(self):
        return super(StockPicking, self).button_validate()

    @api.multi
    def button_validate(self):
        partner = self.partner_id

        if self.get_credit_do_warning_type() == 'none':
            # return self.validate()
            return super(StockPicking, self).button_validate()

        inv_rec = self.env['account.invoice'].search([
            ('partner_id', '=', partner.id),
            ('state', 'not in', ['draft', 'cancel'])
        ])

        s = self.env['sale.order'].search([
            ('origin', '=', self.origin),
        ])

        sale_amount = s.search([
            ('partner_id', '=', partner.id),
        ]).mapped('amount_total')

        cr = CreditLimit()
        is_credit_so_reached = cr.is_credit_so_reached(partner, inv_rec, sale_amount)
        if is_credit_so_reached and (self.get_credit_do_warning_type() == 'warning'):
            return self.show_warning_message()

        return False
