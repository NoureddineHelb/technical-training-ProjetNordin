from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manager_level = fields.Selection(related='partner_id.manager_level')

    def _create_calendar_event(self, line):
        if not line.training_date:
            raise ValidationError("La date est manquante ou invalide.")
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

    def _check_manager_level(self):
        if self.amount_total < 500:
            # confirme la commande direct
            return True
        elif 500 <= self.amount_total < 2000:
            if self.partner_id.manager_level in ('level1', 'level2', 'level3'):
                return True
            else:
                # message d'erreur
                raise ValidationError("La commande de vente doit être confirmée par un manager de niveau 1 ou supérieur")
        elif 2000 <= self.amount_total < 5000:
            if self.partner_id.manager_level in ('level2', 'level3'):
                return True
            else:
                raise ValidationError("La commande de vente doit être confirmée par un manager de niveau 2 ou supérieur")
        else:
            if self.partner_id.manager_level == 'level3':
                return True
            else:
                raise ValidationError("La commande de vente doit être confirmée par un manager de niveau 3")

    def _check_max_order_amount(self):
        for order in self:
            if order.partner_id.user_ids and 'partenaires' in [group.name for group in order.partner_id.user_ids[0].groups_id]:
                max_order_amount = 250
            else:
                max_order_amount = order.partner_id.max_order_amount
            if max_order_amount and order.amount_total > max_order_amount:
                raise ValidationError("Le montant total de la commande dépasse le montant maximal autorisé pour ce partenaire.")

    def action_confirm(self):
        for line in self.order_line:
            if line.employee_id:
                self._create_calendar_event(line)

        if self._check_manager_level():
            super().action_confirm()
        self._check_max_order_amount()