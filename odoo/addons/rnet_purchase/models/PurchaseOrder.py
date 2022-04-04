from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    gut_qty_total = fields.Integer('Quantity Ordered', compute='_get_qty_total')
    gut_qty_received = fields.Integer('Quantity Received', compute='_get_qty_received')
    gut_qty_billed = fields.Integer('Quantity Billed', compute='_get_qty_billed')
    gut_receive_status = fields.Char('Receive Status', compute='_get_receive_status')
    gut_qc = fields.Selection([
        ('Yes','Yes'),
        ('No','No'),
    ], string='Quality Control', default='Yes', required=True)
    gut_term_of_delivery = fields.Selection([
        ('allowed','Partial Delivery Allowed'),
        ('not allowed', 'Partial Delivery Not Allowed'),
    ], string='Term of Delivery', default='allowed', required=True)
    num_word = fields.Char(string="Say:", compute='_compute_amount_in_word')
    gut_description = fields.Text(string='Description')
    total_purchase_product = fields.Integer(string='Total Products:',compute='_total_purchase_product',help="total Products")
    total_purchase_quantity = fields.Integer(string='Total Quantities:',compute='_total_purchase_product_qty',help="total Quantity")


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

    @api.multi
    def _compute_amount_in_word(self):
        for rec in self:
            rec.num_word = str(rec.currency_id.amount_to_text(rec.amount_total))

    def _total_purchase_product(self):
            for record in self:
                list_of_product=[]
                for line in record.order_line:
                    list_of_product.append(line.product_id)
                record.total_purchase_product = len(set(list_of_product))

    def _total_purchase_product_qty(self):
            for record in self:
                total_qty = 0
                for line in record.order_line:
                    total_qty = total_qty + line.product_qty
                record.total_purchase_quantity = total_qty

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    gut_remark = fields.Char('Remark')

class PartnerFax(models.Model):
    _inherit = 'res.partner'
    fax = fields.Char('Fax')