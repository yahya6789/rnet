# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
import logging
_logger = logging.getLogger(__name__)

class AssetTransfer(models.Model):
    _inherit = 'asset.accountability.transfer'

    gut_source_location = fields.Many2one('stock.location', 'Source Location')
    gut_dest_location = fields.Many2one('stock.location', 'Destination Location')
    gut_source_document = fields.Char('Source Document')
    gut_asset_lines_id = fields.Many2one('stock.picking', 'Asset Lines Id')

    @api.multi
    def act_done(self):
        super(AssetTransfer, self).act_done()
        for rec in self:
            rec.transferred_asset_id.write({
                'gut_source_location': rec.gut_dest_location.id
            })

    @api.onchange('asset_transfer_type_id')
    def onchange_asset_transfer_type_id(self):
        res = {
            'domain' : {
                'asset_transfer_type_id' : [('gut_is_system', '=', False)],
            }
        }
        return res

class AssetTransferType(models.Model):
    _inherit = 'asset.transfer.type'

    gut_is_system = fields.Boolean('Is System')