from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    project = fields.Many2one('project.project', string='Project')

    @api.multi
    def request_stock(self):
        stock_obj = self.env['stock.picking']
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
        for rec in self:
            if not rec.requisition_line_ids:
                raise Warning(_('Please create some requisition lines.'))
            if any(line.requisition_type == 'internal' for line in rec.requisition_line_ids):
                if not rec.location_id.id:
                    raise Warning(_('Select Source location under the picking details.'))
                if not rec.custom_picking_type_id.id:
                    raise Warning(_('Select Picking Type under the picking details.'))
                if not rec.dest_location_id:
                    raise Warning(_('Select Destination location under the picking details.'))

                picking_vals = {
                    'partner_id': rec.employee_id.address_home_id.id,
                    'min_date': fields.Date.today(),
                    'location_id': rec.location_id.id,
                    'location_dest_id': rec.dest_location_id and rec.dest_location_id.id or rec.employee_id.dest_location_id.id or rec.employee_id.department_id.dest_location_id.id,
                    'picking_type_id': rec.custom_picking_type_id.id,  # internal_obj.id,
                    'note': rec.reason,
                    'custom_requisition_id': rec.id,
                    'origin': rec.name,
                    'company_id': rec.company_id.id,

                }
                stock_id = stock_obj.sudo().create(picking_vals)
                delivery_vals = {'delivery_picking_id': stock_id.id,}
                rec.write(delivery_vals)

            po_dict = {}
            for line in rec.requisition_line_ids:
                if line.requisition_type == 'purchase':
                    if not line.partner_id:
                        raise Warning(_('Please enter atleast one vendor on Requisition Lines for Requisition Action Purchase.'))
                    for partner in line.partner_id:
                        if partner not in po_dict:
                            po_vals = {
                                'partner_id': partner.id,
                                'currency_id': rec.env.user.company_id.currency_id.id,
                                'date_order': fields.Date.today(),
                                # 'company_id':rec.env.user.company_id.id,
                                'company_id': rec.company_id.id,
                                'custom_requisition_id': rec.id,
                                'origin': rec.name,
                                'project': rec.project.id,
                            }
                            purchase_order = purchase_obj.create(po_vals)
                            po_dict.update({partner: purchase_order})
                            po_line_vals = rec._prepare_po_line(line, purchase_order)
                            purchase_line_obj.sudo().create(po_line_vals)
                        else:
                            purchase_order = po_dict.get(partner)
                            po_line_vals = rec._prepare_po_line(line, purchase_order)
                            purchase_line_obj.sudo().create(po_line_vals)
                rec.state = 'stock'
