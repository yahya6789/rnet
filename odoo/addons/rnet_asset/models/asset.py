# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class Asset(models.Model):
    _inherit = 'account.asset.asset.custom'

    _sql_constraints = [('custom_number_uniq', 'unique (custom_number)', "Asset No must be unique!"), ]
    custom_number = fields.Char(string='Number', readonly=False, required=True)

    gut_product_category = fields.Many2one('product.category', string='Product Category', required=False, readonly=True, states={'draft': [('readonly', False)]})
    gut_product_mapping = fields.Many2one('product.product', 'Product Mapping')
    gut_calibration_certificate = fields.Boolean(string='Calibration Certificate', default=False)
    gut_condition_desc = fields.Char(string='Condition Desc.', required=False, readonly=True, states={'draft': [('readonly', False)]})
    gut_status = fields.Many2one('gut.asset.status', string='Status', required=False)
    gut_condition = fields.Many2one('gut.asset.condition', string='Condition', required=False)
    gut_longitude = fields.Float(string='Longitude', default=0.0)
    gut_latitude = fields.Float(string='Latitude', default=0.0)
    gut_last_calibration = fields.Date(string='Last Calibration', compute='_get_last_calibration')
    gut_source_location = fields.Many2one('stock.location', string='Source Location')
    gut_calibration_count = fields.Integer(compute='_gut_calibration_count', string='# Calibration Count')
    gut_auto_depreciation = fields.Boolean(string='Automatic Depreciation Process', default=True)
    gut_total_terdepresiasi = fields.Float(compute='_compute_total_depreciation', string='Total Terdepresiasi')
    gut_unposted = fields.Float(compute='_compute_unposted', string='Unposted')
    gut_sisa_depresiasi = fields.Float(compute='_compute_sisa_depresiasi', string='Sisa Depresiasi')
    gut_calibration_interval = fields.Integer(string='Calibration Interval')
    gut_recalibration_schedule = fields.Date(string='Recalibration Schedule')
    gut_calibration_product_mapping = fields.Many2one('product.product', 'Calibration Product Mapping')
    gut_calibration_notes = fields.Text('Calibration Notes')
    gut_manufactured_year = fields.Integer("Manufactured Year")

    @api.multi
    def open_calibration_form(self):
        """
        for asset in self:
            return {
                'name': _('Asset Calibration'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'gut.asset.calibration',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'domain': [('asset', '=', asset.id)],
                'option': {'no_create_edit': True}
            }
        """
        pass

    def _get_last_calibration(self):
        """
        for record in self:
            calibration = self.env['gut.asset.calibration'].search([('asset', '=', record.id)], order='date DESC', limit=1)
            if len(calibration) > 0:
                record.gut_last_calibration = calibration.date
            else:
                record.gut_last_calibration = None
        """
        for record in self:
            record.gut_last_calibration = None

    def update_additional_info(self, info):
        self.custom_source_partner_id = info['custodian']
        self.custom_source_department_id = info['department']
        self.gut_source_location = info['location']
        return

    @api.multi
    def _gut_calibration_count(self):
        """
        res = self.env['gut.asset.calibration'].search_count([('asset', '=', self.id)])
        self.gut_calibration_count = res or 0
        """
        self.gut_calibration_count = 0

    @api.multi
    def name_get(self):
        data = []
        for asset in self:
            display_name = '['
            display_name += asset.custom_number or ""
            display_name += '] '
            display_name += asset.name or ""
            data.append((asset.id, display_name))
        return data

    @api.model
    def compute_generated_entries(self, date, asset_type=None):
        created_move_ids = []
        type_domain = []
        if asset_type:
            type_domain = [('type', '=', asset_type)]

        ungrouped_assets = self.env['account.asset.asset.custom'].search(
            type_domain + [('state', '=', 'open'), ('category_id.group_entries', '=', False),
                           ('gut_auto_depreciation', '=', True)])
        created_move_ids += ungrouped_assets._compute_entries(date, group_entries=False)

        for grouped_category in self.env['account.asset.category.custom'].search(
                type_domain + [('group_entries', '=', True)]):
            assets = self.env['account.asset.asset.custom'].search(
                [('state', '=', 'open'), ('category_id', '=', grouped_category.id),
                 ('gut_auto_depreciation', '=', True)])
            created_move_ids += assets._compute_entries(date, group_entries=True)
        return created_move_ids

    @api.one
    def _compute_total_depreciation(self):
        amount = 0
        lines = filter(self.filter_total_depreciation, self.depreciation_line_ids)
        for line in lines:
            amount = amount + line.amount
        self.gut_total_terdepresiasi = amount

    @api.one
    def _compute_unposted(self):
        amount = 0
        lines = filter(self.filter_unposted, self.depreciation_line_ids)
        for line in lines:
            amount = amount + line.amount
        self.gut_unposted = amount

    @api.one
    def _compute_sisa_depresiasi(self):
        amount = 0
        lines = filter(self.filter_sisa_depresiasi, self.depreciation_line_ids)
        for line in lines:
            amount = amount + line.amount
        self.gut_sisa_depresiasi = amount

    def filter_total_depreciation(self, line):
        return line.move_check == True or line.move_posted_check == True

    def filter_unposted(self, line):
        return line.move_check == True and line.move_posted_check == False

    def filter_sisa_depresiasi(self, line):
        return line.move_check == False and line.move_posted_check == False

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('custom_number', operator, name), ('name', operator, name)]
        object_ids = self._search(domain + args, limit=limit)
        return self.browse(object_ids).name_get()
