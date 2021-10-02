from odoo import models, fields, api, tools, _

import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisitionLine(models.Model):
    _name = 'vw.purchase.requisition.lines'
    _auto = False

    id = fields.Integer(string="#")
    req_name = fields.Char(string="Requisition")
    dept_id = fields.Integer(string="Department ID")
    dept_name = fields.Char(string="Department")
    prod_id = fields.Integer(string="Product ID")
    prod_name = fields.Char(string="Product")
    desc = fields.Char(string="Description")
    qty = fields.Float(string="Quantity")

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'vw_purchase_requisition_lines')
        self._cr.execute(""" CREATE OR REPLACE VIEW public.vw_purchase_requisition_lines AS
            select
                row_number() over () as id,
                req."name" as req_name,
                dept.id as dept_id,
                dept."name" as dept_name,
                reql.product_id as prod_id,
                concat('[',templ.default_code,']',' ',templ.name) as prod_name,
                reql.description as "desc",
                reql.qty as qty
            from
                material_purchase_requisition req
            left join hr_department dept on
                req.department_id = dept.id 
            left join material_purchase_requisition_line reql on
                req.id = reql.requisition_id
            left join product_product prod on
                reql.product_id = prod.id
            left join product_template templ on
                prod.product_tmpl_id = templ.id
            where
                req.state::text = 'approve'::text
        """)

    @api.multi
    def open_wizard(self):
        pass
