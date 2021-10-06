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
        names = []
        for req in requisitions:
            if req.name not in names:
                names.append(req.name)

        values = {
            'partner_id': self.vendor_id.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'date_order': fields.Date.today(),
            'company_id': self.company_id.id,
            # 'custom_requisition_id': rec.id,
            'origin': ",".join(names),
        }
        return self.env['purchase.order'].sudo().create([values])

    """
    - Grup/merge quantity unit untuk PR lines (products) yang sama
        menjadi satu line (product).
    """
    def _prepare_po_lines(self, purchase_order, req_lines):
        lines = []
        for line in req_lines:
            value = {
                'product_id': line.product_id.id,
                'name': line.product_id.name,
                'product_qty': line.qty,
                'product_uom': line.uom.id,
                'date_planned': fields.datetime.now(),
                'price_unit': line.product_id.standard_price,
                'order_id': purchase_order.id,
                # 'account_analytic_id': self.analytic_account_id.id,
                'custom_requisition_line_id': line.id
            }
            lines.append(value)

        values = []
        for line in lines:
            line_exist_id = None
            line_exist = False

            for value in values:
                if value.get('product_id') == line.get('product_id'):
                    line_exist_id = line.get('product_id')
                    line_exist = True

            if line_exist:
                # sum
                for value in values:
                    if value.get('product_id') == line_exist_id:
                        qty = value.get('product_qty') + line.get('product_qty')
                        value.update({
                            'product_qty': qty
                        })
            else:
                values.append(line)

        return values

    def _create_po_lines(self, purchase_order, req_lines):
        lines = []
        values = self._prepare_po_lines(purchase_order, req_lines)
        for value in values:
            obj = self.env['purchase.order.line']
            lines.append(obj.sudo().create([value]))
        return lines

    """
    - Tandai PR line (product) yang telah dibuatkan PO nya.
    - Update state PR kalau semua PR line telah dibuatkan PO nya
        dan tidak ada internal picking.
    """
    def _update_requisition(self, requisitions, req_lines):
        selected_requisition_line_ids = [line.id for line in req_lines]

        for req in requisitions:
            for line in req.requisition_line_ids:
                if line.id in selected_requisition_line_ids:
                    line.write({"has_po": True})

        for req in requisitions:
            is_update_state = True
            for line in req.requisition_line_ids:
                # _logger.info("Line " + str(line.id) + " has PO: " + str(line.has_po))
                if not line.has_po:
                    is_update_state = False
                    break
            if is_update_state:
                # _logger.info("Requisition " + req.name + " is empty, updating state")
                req.write({"state": "stock"})

    @api.multi
    def create_po(self):
        # _logger.info("==================================")

        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        req_lines = self.env['material.purchase.requisition.line'].browse(active_ids)
        req_ids = [line.requisition_id.id for line in req_lines]
        requisitions = self.env['material.purchase.requisition'].browse(req_ids)

        po = self._create_po(requisitions)
        if po:
            self._create_po_lines(po, req_lines)
            self._update_requisition(requisitions, req_lines)

        # _logger.info("==================================")
        return {'type': 'ir.actions.act_window_close'}
