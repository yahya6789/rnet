from odoo import models, fields, api, tools, _

import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisitionLineWizard(models.TransientModel):
    _name = "purchase.requisition.line.wizard"

    vendor_id = fields.Many2one("res.partner", "Vendor", domain="[('supplier','=',True)]")
    warehouse_id = fields.Many2one("stock.warehouse", "Warehouse")
    company_id = fields.Many2one('res.company', string='Company', change_default=True, readonly=True,
                                 default=lambda self: self.env.user.company_id.id)

    @api.multi
    @api.onchange('vendor_id')
    def partner_id_change(self):
        wh = self.env['stock.warehouse']
        wh_exist = wh.sudo().search([('company_id', '=', self.company_id.id)], limit=1)
        if wh_exist:
            self.warehouse_id = wh_exist.id

    def _create_po(self, requisitions):
        names = [req.name for req in requisitions]
        values = {
            'partner_id': self.vendor_id.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'date_order': fields.Date.today(),
            'company_id': self.company_id.id,
            # 'custom_requisition_id': rec.id,
            'origin': ",".join(names),
        }
        return self.env['purchase.order'].sudo().create([values])

    def _create_po_lines(self, purchase_order, req_lines):
        lines = []
        obj = self.env['purchase.order.line']
        for line in req_lines:
            values = {
                'product_id': line.product_id.id,
                'name': line.product_id.name,
                'product_qty': line.qty,
                'product_uom': line.uom.id,
                'date_planned': fields.Date.today(),
                'price_unit': line.product_id.standard_price,
                'order_id': purchase_order.id,
                # 'account_analytic_id': self.analytic_account_id.id,
                'custom_requisition_line_id': line.id
            }
            lines.append(obj.sudo().create([values]))
        return lines

    def _update_requisition(self, requisitions, po_lines):
        po_line_ids = [po_line.id for po_line in po_lines]
        # _logger.info("PO Lines: " + str(po_line_ids))

        for req in requisitions:
            pr_line_ids = [req_line.id for req_line in req.requisition_line_ids]
            # _logger.info("PR Lines: " + str(pr_line_ids))
            intersect_line_ids = [value for value in pr_line_ids if value in po_line_ids]
            # _logger.info("Intersect Lines: " + str(intersect_line_ids))

            for line in req.requisition_line_ids:
                if line.id in intersect_line_ids:
                    # _logger.info("Unlinking " + str(line.id))
                    line.unlink()

            if not req.requisition_line_ids:
                # _logger.info("Requisition " + req.name + " is empty, updating state")
                req.write({"state": "stock"})

    @api.multi
    def create_po(self):
        # _logger.info("==================================")

        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        req_lines = self.env['material.purchase.requisition.line'].browse(active_ids)
        req_ids = [req_line.requisition_id.id for req_line in req_lines]
        requisitions = self.env['material.purchase.requisition'].browse(req_ids)

        po = self._create_po(requisitions)
        if po:
            self._create_po_lines(po, req_lines)
            self._update_requisition(requisitions, req_lines)

        # _logger.info("==================================")
        return {'type': 'ir.actions.act_window_close'}
