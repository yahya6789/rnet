# from odoo import models, api, fields
# import logging

# _logger = logging.getLogger(__name__)


# class PurchaseHistoryReport(models.AbstractModel):
#     _name = 'report.ogut_asset.report_purchase_order_history'

#     @api.model
#     def _get_report_values(self, docids, data=None):
#         docs = self.env['purchase.order.history'].browse(docids)
#         return {
#             'doc_ids': docs.ids,
#             'doc_model': 'purchase.order.history',
#             'o': docs,
#             'data': data,
#             'report_type': data.get('report_type') if data else '',
#         }
