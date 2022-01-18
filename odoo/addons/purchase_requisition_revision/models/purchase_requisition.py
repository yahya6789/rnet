# Copyright 2013 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# Copyright 2018 Dreambits Technologies Pvt. Ltd. (<http://dreambits.in>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisition(models.Model):
    _inherit = "material.purchase.requisition"

    @api.model
    def create(self, values):
        return super(PurchaseRequisition, self).create(values)

    @api.depends('current_revision_id', 'old_revision_ids')
    def _compute_has_old_revisions(self):
        for requisition in self:
            if requisition.old_revision_ids:
                requisition.has_old_revisions = True

    @api.one
    @api.depends('old_revision_ids')
    def _compute_revision_count(self):
        self.revision_count = len(self.old_revision_ids)

    current_revision_id = fields.Many2one(
        comodel_name='material.purchase.requisition',
        string='Current revision',
        readonly=True,
        copy=True
    )
    old_revision_ids = fields.One2many(
        comodel_name='material.purchase.requisition',
        inverse_name='current_revision_id',
        string='Old revisions',
        readonly=True,
        context={'active_test': False}
    )
    revision_number = fields.Integer(
        string='Revision',
        copy=False,
        default=0
    )
    unrevisioned_name = fields.Char(
        string='Original Order Reference',
        copy=True,
        readonly=True,
        default='New'
    )
    active = fields.Boolean(
        default=True
    )
    has_old_revisions = fields.Boolean(
        compute='_compute_has_old_revisions')

    revision_count = fields.Integer(compute='_compute_revision_count')

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        return super(PurchaseRequisition, self).copy(default=default)

    def copy_revision_with_context(self):
        default_data = self.default_get([])
        new_rev_number = self.revision_number + 1
        default_data.update({
            'revision_number': new_rev_number,
            'unrevisioned_name': self.unrevisioned_name,
            'name': '%s(REV-%02d)' % (self.unrevisioned_name, new_rev_number),
            'old_revision_ids': [(4, self.id, False)],
        })

        new_revision = self.copy(default_data)
        self.old_revision_ids.write({
            'current_revision_id': new_revision.id,
        })
        self.write({'active': False,
            'state': 'cancel',
            'current_revision_id': new_revision.id,
        })

        return new_revision

    @api.multi
    def create_revision(self):
        revision_ids = []
        # Looping over purchase order records
        for purchase_requisition_rec in self:
            # Calling  Copy method
            copied_purchase_rec = purchase_requisition_rec.copy_revision_with_context()

            msg = _('New revision created: %s') % copied_purchase_rec.name
            copied_purchase_rec.message_post(body=msg)
            purchase_requisition_rec.message_post(body=msg)

            revision_ids.append(copied_purchase_rec.id)

        action = {
            'type': 'ir.actions.act_window',
            'name': _('New Purchases Requisition Revisions'),
            'res_model': 'material.purchase.requisition',
            'domain': "[('id', 'in', %s)]" % revision_ids,
            'auto_search': True,
            # 'views': [
            #     (self.env.ref('purchase.purchase_order_tree').id, 'tree'),
            #     (self.env.ref('purchase.purchase_order_form').id, 'form')],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'nodestroy': True,
        }

        # Returning the new purchase order view with new record.
        return action

    @api.multi
    def open_revision_list(self):
        if self.old_revision_ids:
            for pr in self:
                return {
                    'name': _('Revision History'),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'material.purchase.requisition',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'domain': ['&', ['current_revision_id', '=', pr.id], ['active', '=', False]],
                    'option': {'no_create_edit': True},
                }
