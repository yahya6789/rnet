from odoo import models, fields, api, _

import logging


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    project = fields.Many2one('project.project', string='Project')
    po_revision_count = fields.Integer(compute='_get_po_revision_count')

    subtot = fields.Monetary(compute='_compute_subtot')
    disc_percent = fields.Float(string='Discount (%)', default=0)
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

    def _get_latest_revision_number(self):
        query = """
            SELECT MAX (poh.revision)
            FROM purchase_order_history poh
            WHERE poh.original_id = %s
        """
        params = [self.id]
        self.env.cr.execute(query, params)
        res = self.env.cr.dictfetchone()
        return res['max']

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
        latest = self._get_latest_revision_number()
        if not latest:
            latest = 0

        query = """
            INSERT INTO purchase_order_history (
                access_token,
                amount_tax,
                amount_total,
                amount_untaxed,
                approve_dept_manager_id,
                approve_director_manager_id,
                approve_finance_manager_id,
                company_id,
                create_date,
                create_uid,
                currency_id,
                custom_requisition_id,
                date_approve,
                date_order,
                date_planned,
                dept_manager_approve_date,
                dept_manager_id,
                dest_address_id,
                director_manager_approve_date,
                director_manager_id,
                finance_manager_approve_date,
                finance_manager_id,
                fiscal_position_id,
                group_id,
                incoterm_id,
                invoice_count,
                invoice_status,
                message_main_attachment_id,
                "name",
                notes,
                origin,
                original_id,
                partner_id,
                partner_ref,
                payment_term_id,
                picking_count,
                picking_type_id,
                po_refuse_date,
                po_refuse_user_id,
                project,
                purchase_user_id,
                refuse_reason_note,
                requisition_id,
                revision,
                revision_date,
                state,
                user_id,
                write_date,
                write_uid
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [
            self.access_token,
            self.amount_tax,
            self.amount_total,
            self.amount_untaxed,
            self.approve_dept_manager_id.id if self.approve_dept_manager_id.id else None,
            self.approve_director_manager_id.id if self.approve_director_manager_id.id else None,
            self.approve_finance_manager_id.id if self.approve_finance_manager_id.id else None,
            self.company_id.id if self.company_id.id else None,
            self.create_date,
            self.create_uid.id,
            self.currency_id.id,
            self.custom_requisition_id.id if self.custom_requisition_id.id else None,
            self.date_approve,
            self.date_order,
            self.date_planned,
            self.dept_manager_approve_date if self.dept_manager_approve_date else None,
            self.dept_manager_id.id if self.dept_manager_id.id else None,
            self.dest_address_id.id if self.dest_address_id.id else None,
            self.director_manager_approve_date if self.director_manager_approve_date else None,
            self.director_manager_id.id if self.director_manager_id.id else None,
            self.finance_manager_approve_date if self.finance_manager_approve_date else None,
            self.finance_manager_id.id if self.finance_manager_id.id else None,
            self.fiscal_position_id.id if self.fiscal_position_id.id else None,
            self.group_id.id if self.group_id.id else None,
            self.incoterm_id.id if self.incoterm_id.id else None,
            self.invoice_count,
            self.invoice_status,
            self.message_main_attachment_id.id if self.message_main_attachment_id.id else None,
            self.name,
            self.notes,
            self.origin,
            self.id,
            self.partner_id.id if self.partner_id.id else None,
            self.partner_ref,
            self.payment_term_id.id if self.payment_term_id.id else None,
            self.picking_count,
            self.picking_type_id.id if self.picking_type_id.id else None,
            self.po_refuse_date if self.po_refuse_date else None,
            self.po_refuse_user_id.id if self.po_refuse_user_id.id else None,
            self.project.id if self.project.id else None,
            self.purchase_user_id.id if self.purchase_user_id.id else None,
            self.refuse_reason_note,
            self.requisition_id.id if self.requisition_id.id else None,
            latest + 1,
            fields.datetime.now(),
            self.state,
            self.user_id.id,
            self.write_date,
            self.write_uid.id,
        ]

        self.env.cr.execute(query, params)
        self.env.cr.commit()
        return True;

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
        self.disc_amount = self.subtot * (self.disc_percent / 100)

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
