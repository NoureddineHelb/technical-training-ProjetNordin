from datetime import timedelta

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            if line.employee_id:
                if not line.employee_id.address_home_id:
                    partner = self.env['res.partner'].create({
                        'name': line.employee_id.name,
                        'email': line.employee_id.work_email,
                        'phone': line.employee_id.work_phone,
                    })
                    line.employee_id.address_home_id = partner.id
                start_datetime = fields.Datetime.to_string(line.training_date)
                end_datetime = fields.Datetime.from_string(start_datetime) + timedelta(hours=8)
                event = self.env['calendar.event'].create({
                    'name': 'Formation - %s' % line.name,
                    'start': start_datetime,
                    'stop': end_datetime,
                    'partner_ids': [(4, line.employee_id.address_home_id.id)],
                })
                line.employee_id.calendar_id = event.id

