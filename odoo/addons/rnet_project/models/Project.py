from odoo import models, fields, api


class ProjectType(models.Model):
    _name = 'project.type'
    _description = 'Product Type'
    name = fields.Char(string='name', required=True)


class ProjectStatus(models.Model):
    _name = 'project.status'
    _description = 'Product Status'
    name = fields.Char(string='name', required=True)


class Project(models.Model):
    _inherit = 'project.project'
    no = fields.Char(string='Project No.', required=True)
    project_type = fields.Many2one('project.type', string='Project Type', required=True)
    project_status = fields.Many2one('project.status', string='Project Status')
    contract_no = fields.Char(string='Contract No.')
    contract_date = fields.Date(string='Contract Date')
    reference_no = fields.Char(string='Reference No.')
    plan_start_date = fields.Date(string='Plan Start Date')
    plan_end_date = fields.Date(string='Plan End Date')
    actual_start_date = fields.Date(string='Actual Start Date')
    actual_end_date = fields.Date(string='Actual End Date')
    description = fields.Char(string='Description')
    parent_project = fields.Many2one('project.project', string='Parent Project')
    spk_no = fields.Char(string='SPK.PO No.')
    spk_date = fields.Date(string='SPK.PO Date.')
    res_currency = fields.Many2one('res.currency', string='Currency', required=True)
    payment_term = fields.Char(string='Term of Payment')
    no_kow1 = fields.Char(string='No. KoW1')
    power_comm = fields.Char(string='Power / Comm')
    customer_pic_tech = fields.Many2one('res.partner', string='Customer PIC Tech', required=True)
    customer_pic_comm = fields.Many2one('res.partner', string='Customer PIC Comm', required=True)
    project_duration = fields.Integer(string='Project Duration', required=True)
    plan_delivery_date = fields.Date(string='Plan Delivery Date')
    actual_delivery_date = fields.Date(string='Actual Delivery Date')
    term_of_delivery = fields.Char(string='Term of Delivery')
    notes = fields.Text(string='Notes')
    project_manager = fields.Many2one('res.users', string='Project Manager', required=True)
    project_coordinator = fields.Many2one('res.users', string='Project Coordinator')
    pic_technical = fields.Many2one('res.users', string='PIC Technical')
    pic_project_cost = fields.Many2one('res.users', string='PIC Project Cost')
    team_member = fields.Many2many('res.users', string='Team Member')

    @api.model
    def create(self, vals):
        proj = super(Project, self).create(vals)
        if not proj.no:
            no = self.env['ir.sequence'].next_by_code('project.no') or None
            proj.write({'no': no})
        return proj

    @api.multi
    def name_get(self):
        data = []
        for o in self:
            display_name = '['
            display_name += o.no or ""
            display_name += '] '
            display_name += o.name or ""
            data.append((o.id, display_name))
        return data

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('no', operator, name), ('name', operator, name)]
        project_ids = self._search(domain + args, limit=limit)
        return self.browse(project_ids).name_get()
