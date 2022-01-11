# Copyright 2013 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# Copyright 2018 Dreambits Technologies Pvt. Ltd. (<http://dreambits.in>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('current_revision_id', 'old_revision_ids')
    def _compute_has_old_revisions(self):
        for purchase_order in self:
            if purchase_order.old_revision_ids:
                purchase_order.has_old_revisions = True

    current_revision_id = fields.Many2one(
        comodel_name='purchase.order',
        string='Current revision',
        readonly=True,
        copy=True
    )
    old_revision_ids = fields.One2many(
        comodel_name='purchase.order',
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

    # _sql_constraints = [
    #     ('revision_unique',
    #      'unique(unrevisioned_name, revision_number, company_id)',
    #      'Order Reference and revision must be unique per Company.'),
    # ]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        return super(PurchaseOrder, self).copy(default=default)

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
        for purchase_order_rec in self:
            # Calling  Copy method
            copied_purchase_rec = purchase_order_rec.copy_revision_with_context()

            msg = _('New revision created: %s') % copied_purchase_rec.name
            copied_purchase_rec.message_post(body=msg)
            purchase_order_rec.message_post(body=msg)

            revision_ids.append(copied_purchase_rec.id)

        action = {
            'type': 'ir.actions.act_window',
            'name': _('New purchases Order Revisions'),
            'res_model': 'purchase.order',
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
