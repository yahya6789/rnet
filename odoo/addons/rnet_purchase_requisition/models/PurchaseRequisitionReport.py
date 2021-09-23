from odoo import models, fields, api, _
from odoo.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisitionReport(models.AbstractModel):
    _name = 'report.rnet_purchase_requisition.purchase_requisition_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        _order = self.env['purchase.order'].search([('id', 'in', docids)])

        state = _order.state
        if state == 'purchase' or state == 'done' or state == 'cancel':
            raise Warning(_('Invalid order state: ' + state))

        _order_line = _order.order_line

        return {
            'order': _order,
            'order_line': _order_line
        }
