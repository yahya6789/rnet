from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class MessageWizard(models.TransientModel):
    _name = "message.wizard"

    message = fields.Text('Message', required=True)

    @api.one
    def action_yes(self):
        current_id = int(self.env.context.get('current_id'))
        current_model = self.env.context.get('current_model')
        rec = self.env[current_model].browse([current_id])
        return rec.confirm()

    @api.one
    def action_no(self):
        return {'type': 'ir.actions.act_window_close'}
