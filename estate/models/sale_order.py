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
                    # utilise l'ID de l'utilisateur actuel ou définit False si tu ne veux pas d'événement dans le calendrier de quiconque
                    user_id = self.env.user.id

                vals = {
                    'name': 'Formation - %s' % line.name,
                    'start': start_datetime,
                    'stop': end_datetime,
                    'partner_ids': [(4, line.employee_id.id)],
                    'participant_ids': [(4, line.employee_id.id)],
                    'privacy': 'confidential',
                    'user_id': user_id,
                }
                event = self.env['calendar.event'].create(vals)
                if not event:
                    raise ValueError("L'événement n'a pas été créé correctement !")
                if event.partner_ids != [(4, line.employee_id.id)] or event.participant_ids != [
                    (4, line.employee_id.id)]:
                    raise ValueError("L'événement n'a pas été attribué correctement aux participants !")




