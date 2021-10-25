# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, exceptions, _
import datetime

import logging

_logger = logging.getLogger(__name__)


class StockLocation(models.Model):
    _inherit = 'stock.location'

    # category id 38 = Inventory
    group_access = fields.Many2one('res.groups', string="Group Access", domain="[('category_id', '=', 38)]")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.one
    @api.depends('move_lines.date_expected')
    def _compute_scheduled_date(self):
        po = self.env['purchase.order'].search([
            ('name', '=', self.origin)
        ], limit=1)
        self.scheduled_date = po.date_planned  # datetime.datetime(1970, 12, 10)
