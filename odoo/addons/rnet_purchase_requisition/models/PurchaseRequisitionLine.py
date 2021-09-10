from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import Warning, UserError

import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisitionLine(models.Model):
    _inherit = 'material.purchase.requisition.line'

    brand = fields.Char ('Brand')
    remark = fields.Char ('Remark')
