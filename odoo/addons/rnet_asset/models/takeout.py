# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Takeout(models.Model):
    _inherit = 'stock.picking'
    _description = 'Asset Takeout'

    gut_purpose = fields.Char('Purpose')
    gut_issued_by = fields.Many2one('res.users', 'Issued By')
    gut_issued_date = fields.Date('Issued Date')
    gut_qc_by = fields.Many2one('res.users', 'QC By')
    gut_qc_date = fields.Date('QC Date')
    gut_approved_by = fields.Many2one('res.users', 'Approved By', required=True)
    gut_approved_date = fields.Date('Approved Date')
    gut_received_by = fields.Many2one('res.users', 'Received By')
    gut_received_date = fields.Date('Received Date')
    gut_asset_lines = fields.One2many(comodel_name='gut.takeout.asset.line', inverse_name='gut_takeout_id',
                                      string='Assets', store=True)
    gut_source_department = fields.Many2one('hr.department', 'Source Department')
    gut_destination_department = fields.Many2one('hr.department', 'Destination Department')
    gut_asset_lines_count = fields.Integer(string='Qty Asset', compute='_get_asset_lines_count')
    gut_inventory_lines_count = fields.Integer(string='Qty Inventory', default=0)

    show_confirm = fields.Boolean(
        compute='_compute_show_confirm',
        help='Technical field used to compute whether the confirm button should be shown.')

    @api.multi
    @api.depends('state', 'move_lines')
    def _compute_show_mark_as_todo(self):
        for picking in self:
            if self.env.uid == self.gut_approved_by.id:
                if not picking.move_lines and not picking.package_level_ids:
                    picking.show_mark_as_todo = False
                if not picking.gut_asset_lines and not picking.package_level_ids:
                    picking.show_mark_as_todo = False
                elif not picking.immediate_transfer and picking.state == 'waiting':
                    picking.show_mark_as_todo = True
                elif picking.state != 'waiting' or not picking.id:
                    picking.show_mark_as_todo = False
                else:
                    picking.show_mark_as_todo = True
            else:
                picking.show_mark_as_todo = False

    @api.multi
    @api.depends('state', 'move_lines')
    def _compute_show_confirm(self):
        for picking in self:
            if not picking.move_lines and not picking.package_level_ids:
                picking.show_confirm = False
            if not picking.gut_asset_lines and not picking.package_level_ids:
                picking.show_confirm = False
            elif not picking.immediate_transfer and picking.state == 'draft':
                picking.show_confirm = True
            elif picking.state != 'draft' or not picking.id:
                picking.show_confirm = False
            else:
                picking.show_confirm = True

    def action_ok(self):
        self.write({'state': 'waiting'})

    def action_confirm(self):
        res = super(Takeout, self).action_confirm()
        if self.state == 'draft':
            self.write({'state': 'assigned'})

        return res

    def _validate_inventory_lines(self):
        total_done = 0
        for line in self.move_lines:
            total_done = total_done + line.quantity_done

        if total_done < 1 and self.move_lines:
            raise ValidationError(_("Total done quantity is 0"))

        # raise ValidationError(_("Validation done"))
        return

    def button_validate(self):
        self._validate_inventory_lines()
        self.ensure_one()
        if self.move_lines and self.move_line_ids:
            res = super(Takeout, self).button_validate()
            if self.gut_asset_lines:
                self._create_asset_movement()
            return res

        self.write({'state': 'done'})
        self._create_asset_movement()
        return

    @api.multi
    def _create_asset_movement(self):
        if self._context.get('type') == 'takeout':
            self._takeout_movement()
            return
        elif self._context.get('type') == 'material':
            self._material_movement()
            return
        return

    def _takeout_movement(self):
        # _logger.info("===== Creating takeout movement =====")
        asset_type = self.env['asset.transfer.type'].search([('code', '=', 'OUT')])
        cust_source = self.env['res.partner'].search([('id', '=', 1)])

        for asset in self.gut_asset_lines:
            self.env['asset.accountability.transfer'].create({
                'transferred_asset_id': asset.asset_id.id,
                'asset_transfer_type_id': asset_type.id,
                'source_department_id': self.gut_source_department.id,
                'gut_source_location': self.location_id.id,
                'destination_department_id': self.gut_destination_department.id,
                'gut_dest_location': self.location_dest_id.id,
                'source_partner_id': cust_source.id,
                'destination_partner_id': self.partner_id.id,
                'transferred_date': self.scheduled_date,
                'gut_source_document': self.name,
                'gut_asset_lines_id': self.id
            })

        info = {'custodian': self.partner_id, 'department': self.gut_destination_department,
                'location': self.location_dest_id}
        asset.asset_id.update_additional_info(info)

        return

    def _material_movement(self):
        # _logger.info("===== Creating material movement =====")
        asset_type = self.env['asset.transfer.type'].search([('code', '=', 'REC')])
        dest_source = self.env['res.partner'].search([('id', '=', 1)])

        for asset in self.gut_asset_lines:
            self.env['asset.accountability.transfer'].create({
                'transferred_asset_id': asset.asset_id.id,
                'asset_transfer_type_id': asset_type.id,
                'source_department_id': self.gut_destination_department.id,
                'gut_source_location': self.location_dest_id.id,
                'destination_department_id': self.gut_source_department.id,
                'gut_dest_location': self.location_id.id,
                'source_partner_id': self.partner_id.id,
                'destination_partner_id': dest_source.id,
                'transferred_date': self.scheduled_date,
                'gut_source_document': self.name,
                'gut_asset_lines_id': self.id
            })

        info = {'custodian': dest_source.id, 'department': self.gut_destination_department,
                'location': self.location_dest_id}
        asset.asset_id.update_additional_info(info)

        return

    @api.onchange('picking_type_id')
    def onchange_picking_type_id(self):
        if self._context.get('type') == 'takeout':
            res = {
                'domain': {
                    'picking_type_id': [('name', '=like', 'Take Out%')],
                }
            }
            return res
        elif self._context.get('type') == 'material':
            res = {
                'domain': {
                    'picking_type_id': [('name', '=like', 'Material %')],
                }
            }
            return res
        pass

    @api.one
    def _get_asset_lines_count(self):
        self.gut_asset_lines_count = len(self.gut_asset_lines)

    @api.one
    def _get_inventory_lines_count(self):
        self.gut_inventory_lines_count = len(self.move_lines)

    """
    @api.one
    def _get_inventory_lines_sum(self):
        total = 0
        for line in self.move_line_ids_without_package:
            total = total + line.qty_done

        self.gut_inventory_lines_count = total
    """

    @api.model
    def create(self, vals):
        if vals.get('origin'):
            order = self.env['purchase.order'].search([('name', '=', vals.get('origin'))])
            if order:
                total = 0
                for line in order.order_line:
                    total = total + line.product_qty
                vals.update({'gut_inventory_lines_count': total})
        return super(Takeout, self).create(vals)
