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
    no = fields.Char(string='Project No.', readonly=True, required=True, default='New')
    type_id = fields.Many2one('project.type', string='Project Type')
    status_id = fields.Many2one('project.status', string='Project Status')
    contract_no = fields.Char(string='Contract No.')
    contract_date = fields.Date(string='Contract Date')
    reference_no = fields.Char(string='Reference No.')
    plan_start_date = fields.Date(string='Plan Start Date')
    plan_end_date = fields.Date(string='Plan End Date')
    actual_start_date = fields.Date(string='Actual Start Date')
    actual_end_date = fields.Date(string='Actual End Date')
    description = fields.Char(string='Description')
    partner_id = fields.Many2one('res.partner', string='Customer')
    spk_no = fields.Char(string='SPK.PO No.')
    spk_date = fields.Date(string='SPK.PO Date.')
    res_currency = fields.Many2one('res.currency', string='Currency')
    payment_term = fields.Char(string='Term of Payment')
    no_kow1 = fields.Char(string='No. KoW1')
    power_comm = fields.Char(string='Power / Comm')

    parent_project_id = fields.Many2one('project.project', string='Parent Project')

    @api.model
    def create(self, vals):
        proj = super(Project, self).create(vals)
        if proj.no == 'New':
            no = self.env['ir.sequence'].next_by_code('project.no') or 'New'
            proj.write({'no': no})
        return proj
