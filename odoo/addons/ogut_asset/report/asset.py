from odoo import models, fields, api, tools

class Asset(models.Model):
    _name = "asset_asset_report_custom"
    _description = "Asset Report"
    _auto = False

    #row
    asset_id = fields.Many2one('account.asset.asset.custom', string='Asset')
    asset_no = fields.Char('Asset No')
    reference = fields.Char('Reference')
    sn = fields.Char('S/N')
    asset_name = fields.Char('Asset Name')
    asset_category = fields.Char('Asset Category')
    asset_category_method_number = fields.Char('Asset Category Age (month)')
    asset_category_method_period = fields.Char('Computation Method')
    product_category = fields.Char('Product Category')
    product_category_complete_name = fields.Char('Product Category Complete')
    asset_age_month_sisa = fields.Char('Age Remaining (month)')
    asset_depre_count_sisa = fields.Char('Depre Remaining Count')
    depre_depreciated_last_date = fields.Date("Latest Deprecated Date")
    asset_receive_date = fields.Date('Asset Received Date')
    gut_condition_name = fields.Char('Asset Condition')
    gut_status_name = fields.Char('Asset Status')
    source_partner = fields.Char('Source Custodian')
    source_location = fields.Char('Asset Condition')
    state = fields.Char('State')
    depline_depreciation_date = fields.Date('Depre Line Date')
    depline_depreciated = fields.Boolean('Depre Line Depreciated Flag')

    #measure
    asset_total = fields.Float('Asset Total')
    asset_depre_sch_total = fields.Float('Total Depreciation Schedule')
    purchased_value = fields.Float('Purchased Amount')
    depre_opbal_value = fields.Float('Depreciation Opbal')
    depre_sch_total_value = fields.Float('Depreciation Scheduled')
    depre_depreciated_value = fields.Float('Depreciation Depreciated Amount')
    value_balance = fields.Float('Asset Balance Amount')
    depline_sch_amount = fields.Float('Depre Line Scheduled Amount')
    depline_depreciated_amount = fields.Float('Depre Line Depreciated Amount')
    depline_depreciated_total = fields.Float('Total Depreciation Depreciated')

    @api.model_cr
    def init(self):
        self._cr.execute("select * from asset_asset_report_custom")