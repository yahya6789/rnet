# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    """
    asset_category_id_custom = asset category di tabel account_asset_category_custom,
    pengganti asset_category yang dobel dari odoo_account_asset dan om_account_asset.
    """
    asset_category_id_custom = fields.Many2one('account.asset.category.custom', string='Asset Category Custom')

    @api.onchange('asset_category_id_custom')
    def onchange_asset_category_id_custom(self):
        if self.invoice_id.type == 'out_invoice' and self.asset_category_id_custom:
            self.account_id = self.asset_category_id_custom.account_asset_id.id
        elif self.invoice_id.type == 'in_invoice' and self.asset_category_id_custom:
            self.account_id = self.asset_category_id_custom.account_asset_id.id

    @api.multi
    def action_move_create(self):
        result = super(models.Model, self).action_move_create()
        for inv in self:
            context = dict(self.env.context)
            context.pop('default_type', None)
            #inv.invoice_line_ids.with_context(context).asset_create()
        return result

    @api.one
    def asset_create(self):
        if self.product_id.is_generate_multiple_asset:
            return self.create_multiple_asset()

        return self.create_asset()

    @api.one
    def create_asset(self):
        #if not self.asset_category_id_custom:
            #raise ValidationError("Asset category cannot blank")

        if self.asset_category_id_custom:
            vals = {
                'name': self.name,
                'code': self.invoice_id.number or False,
                'category_id': self.asset_category_id_custom.id,
                #'category_name': self.asset_category_id_custom.name,
                'value': self.price_subtotal_signed,
                'partner_id': self.invoice_id.partner_id.id,
                'company_id': self.invoice_id.company_id.id,
                'currency_id': self.invoice_id.company_currency_id.id,
                'date': self.invoice_id.date_invoice,
                'invoice_id': self.invoice_id.id,
            }

            changed_vals = self.env['account.asset.asset.custom'].onchange_category_id_values(vals['category_id'])
            vals.update(changed_vals['value'])
            #raise ValidationError("Asset category cannot blank")
            asset = self.env['account.asset.asset.custom'].create(vals)
            if self.asset_category_id.open_asset:
                asset.validate()
        return True

    @api.one
    def create_multiple_asset(self):
        if self.asset_category_id_custom:
            vals = {
                'name': self.name,
                'code': self.invoice_id.number or False,
                'category_id': self.asset_category_id_custom.id,
                #'category_name': self.asset_category_id_custom.name,
                'value': self.price_subtotal_signed,
                'partner_id': self.invoice_id.partner_id.id,
                'company_id': self.invoice_id.company_id.id,
                'currency_id': self.invoice_id.company_currency_id.id,
                'date': self.invoice_id.date_invoice,
                'invoice_id': self.invoice_id.id,
            }

            changed_vals = self.env['account.asset.asset.custom'].onchange_category_id_values(vals['category_id'])
            vals.update(changed_vals['value'])

            assets = set()
            for x in range(int(self.quantity)):
                asset = self.env['account.asset.asset.custom'].create(vals)
                assets.add(asset)

            if self.asset_category_id.open_asset:
                for a in assets:
                    a.validate()
        return True

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
