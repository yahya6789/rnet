from odoo import fields, http, _
from odoo.http import request, Controller


class Portal(Controller):

    @http.route('/picking/preview')
    def preview_picking(self):
        values = {}
        return request.render('wbn.preview_picking', values)
