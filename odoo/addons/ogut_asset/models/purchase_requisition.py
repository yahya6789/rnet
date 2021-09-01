from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    project_related = fields.Boolean('Project Related')
    new_investment = fields.Boolean('New Investment')
    expansion = fields.Boolean('Expansion')
    consumables = fields.Boolean('Consumables')
    is_import = fields.Boolean('Import')
    qc = fields.Boolean('Quality Control')
    replacement = fields.Boolean('Replacement')
    misc = fields.Boolean('Misc.')
    car_rental = fields.Boolean('Car Rental')


