from odoo import models, fields, api, _
from odoo.exceptions import Warning

import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    @api.multi
    def request_stock(self):
        stock_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        for rec in self:
            if not rec.requisition_line_ids:
                raise Warning(_('Please create some requisition lines.'))
            for line in rec.requisition_line_ids:
                if line.requisition_type == 'internal':
                    if line.has_po:
                        continue
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
                    delivery_vals = {
                        'delivery_picking_id': stock_id.id,
                    }
                    rec.write(delivery_vals)
                    line.write({"has_po": True})

                    is_update_state = True
                    for l in rec.requisition_line_ids:
                        if not l.has_po and l.requisition_type == 'purchase':
                            is_update_state = False
                            break
                    if is_update_state:
                        rec.write({"state": "stock"})
