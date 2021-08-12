# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class TakeoutInventoryLine(models.Model):
    _inherit = 'stock.move'
    gut_remarks = fields.Char('Remarks')

class TakeoutAssetLine(models.Model):
    _name = 'gut.takeout.asset.line'

    asset_id = fields.Many2one('account.asset.asset.custom', 'Asset')
    gut_takeout_id = fields.Many2one(comodel_name='stock.picking', string='Takeout Number', ondelete='cascade')

    model = fields.Char('model', related='asset_id.custom_model_number')
    serial = fields.Char('serial', related='asset_id.custom_serial_number')
    number = fields.Char('number', related='asset_id.custom_number')
    remarks = fields.Char('remarks')
    code = fields.Char('reference', related='asset_id.code')
