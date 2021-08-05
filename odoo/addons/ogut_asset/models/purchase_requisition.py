from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class MaterialPurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    project = fields.Many2one('project.project', string='Project')

