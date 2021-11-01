from odoo import fields, models, api, _


class PurchaseRequisitionRejectWizard(models.TransientModel):
    _name = 'purchase.requisition.reject.wizard'

    reject_reason = fields.Text(string="Reject Reason", required=True)

    @api.one
    def action_reject(self):
        pr = self.env['material.purchase.requisition'].browse(self._context['requisition_id'])
        pr.write({
            'state': 'reject',
            'reject_employee_id': self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
            'userreject_date': fields.Date.today(),
            'reject_reason': self.reject_reason,
        })

