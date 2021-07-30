# -*- coding: utf-8 -*-

from odoo import models, api, _
from datetime import date
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def unlink(self):
        lines = self.env['account.asset.depreciation.line.custom'].search([('move_id', '=', self.id)], limit=1)
        for line in lines:
            line.move_check = False

        if lines:
            self.env.cr.commit()

        self.mapped('line_ids').unlink()
        return super(AccountMove, self).unlink()
