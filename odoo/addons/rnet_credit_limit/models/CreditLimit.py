class CreditLimit:
    def is_credit_so_reached(self, partner, inv_rec, sale_amount):
        if partner.credit_limit > 0:
            if partner.credit > partner.credit_limit:
                return True
            else:
                credit = 0
                inv_total_amt = 0

                sale_amt = sum([sale for sale in sale_amount])

                for inv in inv_rec:
                    inv_total_amt += inv.amount_total - inv.residual

                if partner.parent_id and partner.parent_id.credit < 0:
                    credit = partner.parent_id.credit

                elif partner.credit < 0:
                    credit = partner.credit

                total_sales = sale_amt + credit - inv_total_amt

                if total_sales > partner.credit_limit:
                    return True
                else:
                    return False
        else:
            return False

    def get_credit_so_warning_type(self):
        return str(
            self.env['ir.config_parameter'].sudo().get_param('rnet_credit_limit.sales_order_validation_cr') or 'block'
        )
