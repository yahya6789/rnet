from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    account_pettycash_id = fields.Many2one('account.account', string="Account Pettycash",
                                           domain="[('user_type_id', 'ilike', 'Bank and Cash')]")
