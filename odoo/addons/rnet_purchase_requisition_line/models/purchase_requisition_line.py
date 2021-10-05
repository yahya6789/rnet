from odoo import models, fields, api, tools, _


class VwPurchaseRequisitionLine(models.Model):
    _name = 'vw.purchase.requisition.line'
    _auto = False

    id = fields.Integer(string="#")
    requisition_id = fields.Char(string="Requisition ID")
    requisition_name = fields.Char(string="Requisition")
    dept_id = fields.Integer(string="Department ID")
    dept_name = fields.Char(string="Department")
    product_id = fields.Integer(string="Product ID")
    product_name = fields.Char(string="Product")
    uom_id = fields.Integer(string="UOM ID")
    uom_name = fields.Char(string="Unit of Measure")
    description = fields.Char(string="Description")
    qty = fields.Float(string="Quantity")

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'vw_purchase_requisition_line')
        self._cr.execute(""" CREATE OR REPLACE VIEW public.vw_purchase_requisition_line AS
            select
                req."name" as requisition_name,
                concat('[', prod.default_code, ']', ' ', templ."name") as product_name,
                dept.id as dept_id,
                dept."name" as dept_name,
                uom.id as uom_id,
                uom."name" as uom_name,
                reql.*
            from
                material_purchase_requisition_line reql
            left join material_purchase_requisition req on
                reql.requisition_id = req.id
            left join product_product prod on
                reql.product_id = prod.id
            left join product_template templ on
                prod.product_tmpl_id = templ.id
            left join hr_department dept on
                req.department_id = dept.id
            left join uom_uom uom on
                reql.uom = uom.id
            where
                req.state = 'approve'
        """)
