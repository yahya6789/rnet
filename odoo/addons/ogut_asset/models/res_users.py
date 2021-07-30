from odoo import api, models, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class User(models.Model):
    _inherit = 'res.users'

    @api.multi
    def write(self, vals):
        #https://stackoverflow.com/questions/60957430/skip-inheritance-order-call-in-odoo
        #panggil fungsi res.users write di modul Base, skip fungsi res.users write-nya modul HR.
        #return super(models.Model, self).write(vals)
        #_logger.info("===============")
        #_logger.info(super(User, self))
        #_logger.info("===============")

        #Bug: User - Application's Accesses ga bisa disave.
        return super(User, self).write(vals)