from odoo import models,_,fields,api

import logging
_logger = logging.getLogger(__name__)


class Transfer(models.Model):
    _inherit = ['stock.picking']
    gut_initial_demand = fields.Integer('Initial Demand', compute='_get_initial_demand')
    gut_qty_done = fields.Integer('Qty Done', compute='_get_qty_done')
    gut_transfer_status = fields.Char('Transfer Status', compute='_get_transfer_status')

    @api.one
    def _get_initial_demand(self):
        total = 0
        for line in self.move_ids_without_package:
            total = total + line.product_uom_qty
        self.gut_initial_demand = total

    @api.one
    def _get_qty_done(self):
        total = 0
        for line in self.move_ids_without_package:
            total = total + line.quantity_done
        self.gut_qty_done = total

    @api.one
    @api.depends('gut_initial_demand', 'gut_qty_done')
    def _get_transfer_status(self):
        self.gut_transfer_status = 'Open'
        if self.gut_initial_demand == self.gut_qty_done:
            self.gut_transfer_status = 'Closed'

    @api.one
    @api.depends('move_lines.date_expected')
    def _compute_scheduled_date(self):
        super(Transfer, self)._compute_scheduled_date()
        #Kalau statusnya "Waiting" (seperti backorder) maka scheduled date-nya di-set sekarang:
        if self.state == 'confirmed':
            self.scheduled_date = fields.Datetime.now()
