from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manager_level = fields.Selection(related='partner_id.manager_level')

    def action_confirm(self):
        for line in self.order_line:
            if line.employee_id:
                if not line.training_date:
                    raise ValueError("La date est manquante ou invalide.")
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
                    'privacy': 'confidential',
                    'user_id': user_id,
                }
                event = self.env['calendar.event'].create(vals)
                if not event:
                    raise ValueError("L'événement n'a pas été créé correctement !")
                if event.partner_ids != [(4, line.employee_id.id)] != [(4, line.employee_id.id)]:
                    raise ValueError("L'événement n'a pas été attribué correctement aux participants !")

        # Question 2
        if self.amount_total < 500:
            # confirme la commande direct
            super().action_confirm()
        elif 500 <= self.amount_total < 2000:
            if self.partner_id.manager_level in ('level1', 'level2', 'level3'):
                super().action_confirm()
            else:
                raise ValidationError("La commande de vente doit être confirmée par un manager de niveau 1 ou supérieur")
        elif 2000 <= self.amount_total < 5000:
            if self.partner_id.manager_level in ('level2', 'level3'):
                super().action_confirm()
            else:
                raise ValidationError("La commande de vente doit être confirmée par un manager de niveau 2 ou supérieur")
        else:
            if self.partner_id.manager_level == 'level3':
                super().action_confirm()
            else:
                raise ValidationError("La commande de vente doit être confirmée par un manager de niveau 3")