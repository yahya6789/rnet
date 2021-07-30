# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, exceptions, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class Hr(models.Model):
    _inherit = 'hr.employee'

    def _sync_user(self, user):
        #Jangan sinkron employee -> user
        vals = dict(
            #name=user.name,
            #image=user.image,
            #work_email=user.email,import inspect
        )
        if user.tz:
            vals['tz'] = user.tz
        return vals