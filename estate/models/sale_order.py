from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manager_level = fields.Selection(related='partner_id.manager_level')
    activity_ids = fields.One2many('mail.activity', 'res_id', domain=[('res_model', '=', 'sale.order')])

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        # Question 1
        for line in self.order_line:
            if line.employee_id:
                if not line.training_date:
                    raise ValidationError("La date est manquante ou invalide.")
                start_datetime = fields.Datetime.to_string(line.training_date)
                end_datetime = fields.Datetime.from_string(start_datetime) + timedelta(hours=8)
                partner = self.env['res.partner'].search([('name', '=', line.employee_id.name)], limit=1)
                if not partner:
                    raise ValidationError("L'employé sélectionné n'a pas de partenaire ")
                if line.employee_id.user_id:
                    user_id = line.employee_id.user_id.id
                else:
                    user_id = self.env.user.id
                vals = {
                    'name': 'Formation - %s' % line.name,
                    'start': start_datetime,
                    'stop': end_datetime,
                    'partner_ids': [(4, line.employee_id.id)],
                    'privacy': 'confidential',
                    'user_id': user_id,
                    'attendee_ids': [(4, line.employee_id.id)],
                }
                event = self.env['calendar.event'].create(vals)
                if not event:
                    raise ValidationError("L'événement n'a pas été créé correctement !")
                if event.partner_ids != [(4, line.employee_id.id)] != [(4, line.employee_id.id)]:
                    raise ValidationError("L'événement n'a pas été attribué correctement aux participants !")

            # Question 2
            user_groups = self.env.user.groups_id
            if self.amount_total < 500:
                # confirme la commande direct
                super().action_confirm()
            elif 500 <= self.amount_total < 2000:
                if any(group.user_type in ('manager_1', 'manager_2', 'manager_3') for group in user_groups):
                    super().action_confirm()
                else:
                    # message d'erreur
                    raise ValidationError(
                        "La commande de vente doit être confirmée par un manager de niveau 1 ou supérieur")
            elif 2000 <= self.amount_total < 5000:
                if any(group.user_type in ('manager_2', 'manager_3') for group in user_groups):
                    super().action_confirm()
                else:
                    raise ValidationError(
                        "La commande de vente doit être confirmée par un manager de niveau 2 ou supérieur")
            else:
                if any(group.user_type == 'manager_3' for group in user_groups):
                    super().action_confirm()
                else:
                    raise ValidationError("La commande de vente doit être confirmée par un manager de niveau 3")

            # Question 3
            if 'partner' in [group.user_type for group in user_groups] and self.amount_total > 350:
                raise ValidationError("Les partenaires ne peuvent pas passer de commande de plus de 350.")

        return res

    def request_approval(self):
        for group in self.env.user.groups_id:
            if group.user_type != 'manager_3' or group.user_type != 'manager_2' or group.user_type != 'manager_1':
                manager_1_groups = self.env['res.groups'].search([('user_type', '=', 'manager_1')])
                manager_1_users = self.env['res.users'].search([('groups_id', 'in', manager_1_groups.ids)])
                if manager_1_users:
                    # Envoyer l'activité au premier manager_1 trouvé
                    summary = "Demande d'approbation de la commande %s" % self.name
                    body = "Une commande de vente a été soumise à votre approbation. Veuillez vérifier les détails de la commande et confirmer ou refuser sa validation. "
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'note': body,
                        'summary': summary,
                        'res_id': self.id,
                        'res_model_id': self.env.ref('sale.model_sale_order').id,
                        'user_id': manager_1_users[0].id,
                    })
        return True
