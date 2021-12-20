from odoo import fields, models, api, _
from odoo.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisitionRejectWizard(models.TransientModel):
    _name = 'purchase.requisition.reject.wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    reject_reason = fields.Text(string="Reject Reason", required=True)

    @api.one
    def action_reject(self):
        pr = self.env['material.purchase.requisition'].browse(self._context['requisition_id'])
        pr.write({
            'state': 'reject',
            'reject_employee_id': self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)], limit=1).id,
            'userreject_date': fields.Date.today(),
            'reject_reason': self.reject_reason,
        })

        template = self.env.ref('ogut_asset.purchase_requisition_reject_email_template')
        if template:
            template.send_mail(pr.id)
