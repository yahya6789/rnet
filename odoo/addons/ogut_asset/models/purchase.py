from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    project = fields.Many2one('project.project', string='Project')

    subtot = fields.Monetary(compute='_compute_subtot')
    disc_percent = fields.Float(string='Discount', default=0)
    disc_amount = fields.Monetary(compute='_compute_disc')
    subtot_after_disc = fields.Monetary(compute='_compute_subtot_after_disc')
    vat_percent = fields.Float(string='VAT', default=0)
    vat_amount = fields.Monetary(compute='_compute_vat')
    subtot_after_tax = fields.Monetary(compute='_compute_subtot_after_tax')
    freight = fields.Monetary(compute='_get_freight')
    subtot_after_freight = fields.Monetary(compute='_compute_subtot_after_freight')
    total_order = fields.Monetary(compute='_get_total_order')

    responsible_id = fields.Many2one('hr.employee', string='Responsible')

    @api.model
    def create(self, vals):
        return super(models.Model, self).create(vals)

    @api.multi
    def button_confirm(self):
        for order in self:
            if 'New' in order.name:
                sequence = self.env['ir.sequence'].next_by_code('purchase.order') or '/'
                order.write({
                    'name': sequence,
                    # 'unrevisioned_name': sequence
                })

        return super(PurchaseOrder, self).button_confirm()

    @api.depends('order_line.price_total', 'freight')
    def _amount_all(self):
        freight = self.freight
        disc = self.disc_amount
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                if not line.product_id.display_as_delivery_cost:
                    amount_untaxed += line.price_subtotal
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed - disc + amount_tax + freight,
            })

    @api.one
    def _compute_subtot(self):
        for line in self.order_line:
            if not line.product_id.display_as_delivery_cost:
                self.subtot = self.subtot + line.price_subtotal

    @api.one
    @api.depends('subtot', 'disc_percent')
    def _compute_disc(self):
        #self.disc_amount = self.subtot * (self.disc_percent / 100)
        self.disc_amount = self.disc_percent

    @api.one
    @api.depends('subtot', 'disc_amount')
    def _compute_subtot_after_disc(self):
        self.subtot_after_disc = self.subtot - self.disc_amount

    @api.one
    @api.depends('subtot_after_disc', 'vat_percent')
    def _compute_vat(self):
        self.vat_amount = self.amount_tax # self.subtot_after_disc * (self.vat_percent / 100)

    @api.one
    @api.depends('subtot_after_disc', 'vat_amount')
    def _compute_subtot_after_tax(self):
        self.subtot_after_tax = self.subtot_after_disc + self.vat_amount

    @api.one
    def _get_freight(self):
        for line in self.order_line:
            if line.product_id.display_as_delivery_cost:
                self.freight = self.freight + line.price_unit

    @api.one
    @api.depends('subtot_after_tax', 'freight')
    def _compute_subtot_after_freight(self):
        self.subtot_after_freight = self.subtot_after_tax + self.freight

    @api.one
    @api.depends('subtot_after_freight')
    def _get_total_order(self):
        self.total_order = self.subtot_after_freight
