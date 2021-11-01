from odoo import models, fields, api

class PurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    reject_reason = fields.Text(string="Reject Reason", readonly=True)

    @api.multi
    def requisition_reject(self):
        view_id = self.env.ref('ogut_asset.purchase_requisition_reject_wizard').id
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.requisition.reject.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'name': 'Purchase Requisition',
            'views': [[view_id, 'form']],
            'context': {'requisition_id': self.id}
        }
