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
    no = fields.Char(string='Project No.', readonly=False, required=True, default='New')
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
    customer = fields.Many2one('res.partner', string='Customer', required=True)
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

    @api.model
    def create(self, vals):
        proj = super(Project, self).create(vals)
        if proj.no == 'New':
            no = self.env['ir.sequence'].next_by_code('project.no') or 'New'
            proj.write({'no': no})
        return proj
