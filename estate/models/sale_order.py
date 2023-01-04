from datetime import timedelta

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            if line.employee_id:
                start_datetime = fields.Datetime.to_string(line.training_date)
                end_datetime = fields.Datetime.from_string(start_datetime) + timedelta(hours=8)
                if line.employee_id.user_id:
                    user_id = line.employee_id.user_id.id
                else:
                    # utilisez l'ID de l'utilisateur actuel ou définissez-le sur False si vous ne voulez pas de l'événement dans le calendrier de quiconque
                    user_id = self.env.user.id

                event = self.env['calendar.event'].create({
                    'name': 'Formation - %s' % line.name,
                    'start': start_datetime,
                    'stop': end_datetime,
                    'partner_ids': [(4, line.employee_id.id)],
                    'participant_ids': [(4, line.employee_id.id)],
                    'privacy': 'confidential',
                    'user_id': user_id,
                })


