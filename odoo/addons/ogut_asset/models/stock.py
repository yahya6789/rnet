# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, exceptions, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class StockLocation(models.Model):
    _inherit = 'stock.location'

    #category id 38 = Inventory
    group_access = fields.Many2one('res.groups', string="Group Access", domain="[('category_id', '=', 38)]")