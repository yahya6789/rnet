from odoo import models, fields, api, _
from datetime import date
import logging
_logger = logging.getLogger(__name__)

class assetCalibration(models.Model):
    _name = 'gut.asset.calibration'
    _description = 'Asset Calibration'

    sequence = fields.Char('Sequence', readonly=True)
    date = fields.Date('Date', default= date.today(), required=True)
    description = fields.Char('Description')
    asset = fields.Many2one('account.asset.asset.custom', 'Asset', required=True, default=lambda self: self._set_selected_asset(),)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('calibration.seq') or '/'
        vals['sequence'] = seq
        return super(assetCalibration, self).create(vals)

    def _set_selected_asset(self):
        #_logger.info("=== _set_selected_asset ===")
        asset_id = self._context.get('asset_id')
        if asset_id != None:
            return self.env['account.asset.asset.custom'].search([('id', '=', asset_id)], limit=1).id
        return None

    @api.onchange('asset')
    def onchange_asset(self):
        #_logger.info("=== onchange_asset ===")
        asset_id = self._context.get('asset_id')
        if asset_id != None:
            res = {
                'domain' : {
                    'asset' : [('id', '=', asset_id)],
                }
            }
            return res
