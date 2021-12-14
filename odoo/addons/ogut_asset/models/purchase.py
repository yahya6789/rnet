from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    project = fields.Many2one('project.project', string='Project')
    po_revision_count = fields.Integer(compute='_get_po_revision_count')

    subtot = fields.Monetary(compute='_compute_subtot')
    disc_percent = fields.Float(string='Discount', default=0)
    disc_amount = fields.Monetary(compute='_compute_disc')
    subtot_after_disc = fields.Monetary(compute='_compute_subtot_after_disc')
    vat_percent = fields.Float(string='VAT', default=0)
    vat_amount = fields.Monetary(compute='_compute_vat')
    subtot_after_tax = fields.Monetary(compute='_compute_subtot_after_tax')
    freight = fields.Monetary(compute='_get_freight')
    subtot_after_freight = fields.Monetary(compute='_compute_subtot_after_freight')
    total_order = fields.Monetary(compute='_get_total_order')

    responsible_id = fields.Many2one('hr.employee', string='Responsible')

    @api.model
    def create(self, vals):
        return super(models.Model, self).create(vals)

    @api.multi
    def button_confirm(self):
        for order in self:
            sequence = self.env['ir.sequence'].next_by_code('purchase.order') or '/'
            order.write({'name': sequence})

        return super(PurchaseOrder, self).button_confirm()

    @api.one
    def _get_po_revision_count(self):
        res = self.env['purchase.order.history'].search_count([('original_id', '=', self.id)])
        self.po_revision_count = res or 0

    @api.multi
    def open_po_revision_list(self):
        if self.po_revision_count:
            for po in self:
                return {
                    'name': _('Revision History'),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'purchase.order.history',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'domain': [('original_id', '=', po.id)],
                    'option': {'no_create_edit': True},
                }
            pass
        pass

    @api.multi
    def button_make_revision(self):
        self._create_purchase_order_history()
        self._create_purchase_order_line_history()

    def _create_purchase_order_history(self):
        query = """
            insert into purchase_order_history (
                message_main_attachment_id,access_token,"name",origin,partner_ref,date_order,date_approve,partner_id,
                dest_address_id,currency_id,notes,invoice_count,invoice_status,date_planned,amount_untaxed,amount_tax,
                amount_total,fiscal_position_id,payment_term_id,user_id,company_id,custom_requisition_id,incoterm_id,
                picking_count,picking_type_id,group_id,state,po_refuse_user_id,po_refuse_date,refuse_reason_note,
                dept_manager_id,finance_manager_id,director_manager_id,approve_dept_manager_id,approve_finance_manager_id,
                approve_director_manager_id,dept_manager_approve_date,finance_manager_approve_date,
                director_manager_approve_date,purchase_user_id,requisition_id,project,create_uid,create_date,write_uid,
                write_date,disc_percent,vat_percent,responsible_id,original_id,revision,revision_date,gut_qc,gut_term_of_delivery
            ) 
            select 
                message_main_attachment_id,access_token,"name",origin,partner_ref,date_order,date_approve,partner_id,
                dest_address_id,currency_id,notes,invoice_count,invoice_status,date_planned,amount_untaxed,amount_tax,
                amount_total,fiscal_position_id,payment_term_id,user_id,company_id,custom_requisition_id,incoterm_id,
                picking_count,picking_type_id,group_id,state,po_refuse_user_id,po_refuse_date,refuse_reason_note,
                dept_manager_id,finance_manager_id,director_manager_id,approve_dept_manager_id,approve_finance_manager_id,
                approve_director_manager_id,dept_manager_approve_date,finance_manager_approve_date,
                director_manager_approve_date,purchase_user_id,requisition_id,project,create_uid,create_date,write_uid,
                write_date,disc_percent,vat_percent,responsible_id,%s,
                (
                    select case when count(1) > 0 then max(poh.revision) + 1 else 1 end as revision 
                    from purchase_order_history poh where poh.original_id = %s
                ),
                %s,gut_qc,gut_term_of_delivery
            from 
              purchase_order where id = %s
        """
        params = [self.id, self.id, fields.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.id]
        self.env.cr.execute(query, params)
        self.env.cr.commit()

    def _create_purchase_order_line_history(self):
        query = """
            insert into purchase_order_line_history (
                "name","sequence",product_qty,product_uom_qty,date_planned,product_uom, product_id,price_unit,
                price_subtotal,price_total,price_tax,order_id,account_analytic_id,company_id,state, qty_invoiced,
                qty_received,partner_id,currency_id,create_uid,create_date,write_uid,write_date,orderpoint_id,
                sale_order_id,sale_line_id,custom_requisition_line_id,gut_remark,discount
            ) 
            select
                "name","sequence",product_qty,product_uom_qty,date_planned,product_uom,product_id,price_unit,
                price_subtotal,price_total,price_tax,(
                    select poh.id from purchase_order_history poh where poh.original_id = %s order by poh.revision desc limit 1
                ), account_analytic_id,company_id,state,qty_invoiced,qty_received,partner_id,currency_id,create_uid,
                create_date,write_uid,write_date,orderpoint_id,sale_order_id,sale_line_id,custom_requisition_line_id,
                gut_remark,discount 
            from purchase_order_line where order_id = %s
        """
        params = [self.id, self.id]
        self.env.cr.execute(query, params)
        self.env.cr.commit()

    @api.depends('order_line.price_total', 'freight')
    def _amount_all(self):
        freight = self.freight
        disc = self.disc_amount
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                if not line.product_id.display_as_delivery_cost:
                    amount_untaxed += line.price_subtotal
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed - disc + amount_tax + freight,
            })

    @api.one
    def _compute_subtot(self):
        for line in self.order_line:
            if not line.product_id.display_as_delivery_cost:
                self.subtot = self.subtot + line.price_subtotal

    @api.one
    @api.depends('subtot', 'disc_percent')
    def _compute_disc(self):
        #self.disc_amount = self.subtot * (self.disc_percent / 100)
        self.disc_amount = self.disc_percent

    @api.one
    @api.depends('subtot', 'disc_amount')
    def _compute_subtot_after_disc(self):
        self.subtot_after_disc = self.subtot - self.disc_amount

    @api.one
    @api.depends('subtot_after_disc', 'vat_percent')
    def _compute_vat(self):
        self.vat_amount = self.amount_tax # self.subtot_after_disc * (self.vat_percent / 100)

    @api.one
    @api.depends('subtot_after_disc', 'vat_amount')
    def _compute_subtot_after_tax(self):
        self.subtot_after_tax = self.subtot_after_disc + self.vat_amount

    @api.one
    def _get_freight(self):
        for line in self.order_line:
            if line.product_id.display_as_delivery_cost:
                self.freight = self.freight + line.price_unit

    @api.one
    @api.depends('subtot_after_tax', 'freight')
    def _compute_subtot_after_freight(self):
        self.subtot_after_freight = self.subtot_after_tax + self.freight

    @api.one
    @api.depends('subtot_after_freight')
    def _get_total_order(self):
        self.total_order = self.subtot_after_freight
