from odoo import models, fields, api, _
from datetime import date


class AssetCalibration(models.Model):
    _name = 'gut.asset.calibration'
    _description = 'Asset Calibration'

    calibration_request_no = fields.Char('Calibration No.', readonly=True, default='New')
    requisition_date_line = fields.Date('Requisition Date Line', required=True)
    calibration_responsible = fields.Many2one('hr.employee', 'User Responsible', required=True)
    vendor = fields.Many2one('res.partner', 'Vendor', required=True)
    asset_line_ids = fields.One2many(comodel_name='gut.asset.calibration.line', inverse_name='asset_calibration_id', string='Assets')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('pr_created', 'Purchase Request Created'),
        ('closed', 'Closed'), ],
        default='draft',
        track_visibility='onchange',
    )

    @api.model
    def create(self, vals):
        vals['calibration_request_no'] = self.env['ir.sequence'].next_by_code('calibration.seq') or 'New'
        return super(AssetCalibration, self).create(vals)

    @api.multi
    def name_get(self):
        data = []
        for o in self:
            display_name = o.calibration_request_no
            data.append((o.id, display_name))
        return data

    @api.multi
    def action_show_pr(self):
        pass


class AssetCalibrationLine(models.Model):
    _name = 'gut.asset.calibration.line'
    _description = 'Asset Calibration Line'

    asset_calibration_id = fields.Many2one(comodel_name='gut.asset.calibration', index=True, required=True, ondelete='cascade')
    asset_id = fields.Many2one(comodel_name='account.asset.asset.custom', string='Asset', required=True)
    asset_name = fields.Char('Asset Name')
    asset_sn = fields.Char('SN')
    product_name = fields.Char('PR Product')
    last_calibration = fields.Date('Last Calibration')
    recalibration_schedule = fields.Date('Recalibration Schedule')
    recalibration_plan_date = fields.Date('Recalibration Plan Date')
    calibration_actual_date = fields.Date('Calibration Actual Date')
    notes = fields.Char('Notes')

    @api.onchange('asset_id')
    def onchange_asset_id(self):
        for rec in self:
            rec.asset_name = rec.asset_id.name
            rec.asset_sn = rec.asset_id.custom_serial_number
            rec.product_name = rec.asset_id.gut_product_mapping.name
