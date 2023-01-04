from datetime import timedelta

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            if line.employee_id:
                start_datetime = fields.Datetime.to_string(fields.Datetime.now())[:11] + line.training_date.strftime('%Y-%m-%d')
                end_datetime = start_datetime + timedelta(hours=8)
                event = self.env['calendar.event'].create({
                    'name': 'Formation - %s' % line.name,
                    'start': start_datetime,
                    'stop': end_datetime,
                    'partner_ids': [(4, line.employee_id.partner_id.id)],
                })
