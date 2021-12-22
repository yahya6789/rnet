from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import Warning, UserError

import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    project = fields.Many2one('project.project', string='Project')
    vendors = fields.Char(compute='_get_vendors')
    categories = fields.Char(compute='_get_categories')
    product_id = fields.Many2one('product.product', related='requisition_line_ids.product_id', string='Product', readonly=False)

    pr_revision_count = fields.Integer(compute='_get_pr_revision_count')

    @api.model
    def create(self, vals):
        res = super(PurchaseRequisition, self).create(vals)
        list_name = res.name.split('/')
        list_name[2] = res.department_id.name[0:3].upper()
        new_name = '/'
        res.write({
            'name': new_name.join(list_name)
        })
        return res

    @api.one
    def _get_vendors(self):
        vendors = set()
        for line in self.requisition_line_ids:
            for partner_id in line.partner_id:
                vendors.add(partner_id.name)
        self.vendors = ', '.join(vendors)

    @api.one
    def _get_categories(self):
        categories = set()
        for line in self.requisition_line_ids:
            categories.add(line.product_id.categ_id.name)
        self.categories = ', '.join(categories)

    @api.multi
    def request_stock(self):
        self.is_requisition_date_valid()

        stock_obj = self.env['stock.picking']
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
        for rec in self:
            if not rec.requisition_line_ids:
                raise Warning(_('Please create some requisition lines.'))
            if any(line.requisition_type == 'internal' for line in rec.requisition_line_ids):
                if not rec.location_id.id:
                    raise Warning(_('Select Source location under the picking details.'))
                if not rec.custom_picking_type_id.id:
                    raise Warning(_('Select Picking Type under the picking details.'))
                if not rec.dest_location_id:
                    raise Warning(_('Select Destination location under the picking details.'))

                picking_vals = {
                    'partner_id': rec.employee_id.address_home_id.id,
                    'min_date': fields.Date.today(),
                    'location_id': rec.location_id.id,
                    'location_dest_id': rec.dest_location_id and rec.dest_location_id.id or rec.employee_id.dest_location_id.id or rec.employee_id.department_id.dest_location_id.id,
                    'picking_type_id': rec.custom_picking_type_id.id,  # internal_obj.id,
                    'note': rec.reason,
                    'custom_requisition_id': rec.id,
                    'origin': rec.name,
                    'company_id': rec.company_id.id,
                    'gut_issued_by': rec.employee_id.id,
                    'gut_issued_date': rec.request_date,

                }
                stock_id = stock_obj.sudo().create(picking_vals)
                delivery_vals = {'delivery_picking_id': stock_id.id,}
                rec.write(delivery_vals)

            po_dict = {}
            for line in rec.requisition_line_ids:
                if line.requisition_type == 'purchase':
                    if not line.partner_id:
                        raise Warning(_('Please enter atleast one vendor on Requisition Lines for Requisition Action Purchase.'))
                    for partner in line.partner_id:
                        if partner not in po_dict:
                            po_vals = {
                                'partner_id': partner.id,
                                'currency_id': rec.env.user.company_id.currency_id.id,
                                'date_order': fields.Date.today(),
                                # 'company_id':rec.env.user.company_id.id,
                                'company_id': rec.company_id.id,
                                'custom_requisition_id': rec.id,
                                'origin': rec.name,
                                'project': rec.project.id,
                                'responsible_id': self.requisiton_responsible_id.id,
                            }
                            purchase_order = purchase_obj.create(po_vals)
                            po_dict.update({partner: purchase_order})
                            po_line_vals = rec._prepare_po_line(line, purchase_order)
                            purchase_line_obj.sudo().create(po_line_vals)
                        else:
                            purchase_order = po_dict.get(partner)
                            po_line_vals = rec._prepare_po_line(line, purchase_order)
                            purchase_line_obj.sudo().create(po_line_vals)
                rec.state = 'stock'

    @api.onchange('project')
    def on_change_project(self):
        pm = self.project.project_manager
        analytic = self.project.analytic_account

        self.requisiton_responsible_id = pm if pm else None
        self.analytic_account_id = analytic if analytic else None

    def is_requisition_date_valid(self):
        if self.receive_date:
            if self.request_date > self.receive_date:
                raise UserError(_("Received Date cannot earlier than Requisition Date"))

    @api.multi
    def write(self, vals):
        if vals.get('receive_date'):
            receive_date = datetime.strptime(vals.get('receive_date'), '%Y-%m-%d').date()
            if self.request_date > receive_date:
                raise UserError(_("Received Date cannot earlier than Requisition Date"))

        return super(PurchaseRequisition, self).write(vals)

    @api.multi
    def requisition_confirm(self):
        self.is_requisition_date_valid()
        return super(PurchaseRequisition, self).requisition_confirm()

    @api.multi
    def manager_approve(self):
        self.is_requisition_date_valid()
        return super(PurchaseRequisition, self).manager_approve()

    @api.multi
    def user_approve(self):
        self.is_requisition_date_valid()
        return super(PurchaseRequisition, self).user_approve()

    @api.one
    def _get_pr_revision_count(self):
        res = self.env['purchase.requisition.history'].search_count([('original_id', '=', self.id)])
        self.pr_revision_count = res or 0

    @api.multi
    def open_pr_revision_list(self):
        pass
        """
        if self.pr_revision_count:
            for pr in self:
                return {
                    'name': _('Revision History'),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'purchase.requisition.history',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'domain': [('original_id', '=', pr.id)],
                    'option': {'no_create_edit': True},
                }
        """

    @api.multi
    def button_make_revision(self):
        self._create_requisition_history()
        self._create_requisition_line_history()

    def _create_requisition_history(self):
        query = """
        insert into purchase_requisition_history (
            message_main_attachment_id,access_token,"name",state,request_date,department_id,employee_id,
            approve_manager_id,reject_manager_id,approve_employee_id,reject_employee_id,company_id,location_id,date_end,
            date_done,managerapp_date,manareject_date,userreject_date,userrapp_date,receive_date,reason,analytic_account_id,
            dest_location_id,delivery_picking_id,requisiton_responsible_id,employee_confirm_id,confirm_date,
            custom_picking_type_id,create_uid,create_date,write_uid,write_date,maintenance_id,project,
            reject_reason,original_id,revision,revision_date)
        select 
            message_main_attachment_id,access_token,"name",state,request_date,department_id,employee_id,
            approve_manager_id,reject_manager_id,approve_employee_id,reject_employee_id,company_id,location_id,
            date_end,date_done,managerapp_date,manareject_date,userreject_date,userrapp_date,receive_date,
            reason,analytic_account_id,dest_location_id,delivery_picking_id,requisiton_responsible_id,employee_confirm_id,
            confirm_date,custom_picking_type_id,create_uid,create_date,write_uid,write_date,maintenance_id,project,reject_reason,
            %s,(
                select case when count(1) > 0 then max(pr.revision) + 1 else 1 end as revision 
                from purchase_requisition_history pr where pr.original_id = %s
            ),%s
            from material_purchase_requisition pr where pr.id = %s
        """
        params = [self.id, self.id, fields.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.id]
        self.env.cr.execute(query, params)
        self.env.cr.commit()

    def _create_requisition_line_history(self):
        query = """
            insert into purchase_requisition_line_history (
                product_id,description,qty,uom,requisition_type,brand,brand_note,remark,requisition_id,create_uid,
                create_date,write_uid,write_date)
            select
                product_id,description,qty,uom,requisition_type,brand,brand_note,remark,(
                    select pr.id from purchase_requisition_history pr where pr.original_id = %s 
                    order by pr.revision desc limit 1
                ) as requisition_id,create_uid,create_date,write_uid,write_date
            from material_purchase_requisition_line prl where prl.requisition_id = %s
        """
        params = [self.id, self.id]
        self.env.cr.execute(query, params)
        self.env.cr.commit()

    @api.multi
    def open_pr_revision_list(self):
        if self.pr_revision_count:
            for pr in self:
                return {
                    'name': _('Revision History'),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'purchase.requisition.history',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'domain': [('original_id', '=', pr.id)],
                    'option': {'no_create_edit': True},
                }
