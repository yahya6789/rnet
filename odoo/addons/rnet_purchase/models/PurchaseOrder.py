from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    gut_qty_total = fields.Integer('Quantity Ordered', compute='_get_qty_total')
    gut_qty_received = fields.Integer('Quantity Received', compute='_get_qty_received')
    gut_qty_billed = fields.Integer('Quantity Billed', compute='_get_qty_billed')
    gut_receive_status = fields.Char('Receive Status', compute='_get_receive_status')
    gut_qc = fields.selection([
        ('Yes','Yes'),
        ('No','No'),
    ], string='Quality Control')
    gut_term_of_delivery = fields.selection([
        ('allowed','Partial Delivery Allowed'),
        ('not allowed', 'Partial Delivery Not Allowed'),
    ], string='Term of Delivery')

    @api.one
    def _get_qty_total(self):
        total = 0
        for line in self.order_line:
            total = total + line.product_uom_qty
        self.gut_qty_total = total

    @api.one
    def _get_qty_received(self):
        total = 0
        for line in self.order_line:
            total = total + line.qty_received
        self.gut_qty_received = total

    @api.one
    def _get_qty_billed(self):
        total = 0
        for line in self.order_line:
            total = total + line.qty_invoiced
        self.gut_qty_billed = total

    @api.one
    @api.depends('gut_qty_total', 'gut_qty_received')
    def _get_receive_status(self):
        if self.gut_qty_received < self.gut_qty_total:
            self.gut_receive_status = 'Open'
        elif self.gut_qty_received == self.gut_qty_total:
            self.gut_receive_status = 'Close'
        elif self.gut_qty_received > self.gut_qty_total:
            self.gut_receive_status = 'Over'
        else:
            self.gut_receive_status = None


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    gut_remark = fields.Char('Remark')
