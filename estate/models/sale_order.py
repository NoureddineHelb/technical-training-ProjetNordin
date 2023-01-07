#sale_order.py :
from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manager_level = fields.Selection(related='partner_id.manager_level')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            if not line.training_date:
                raise ValidationError("La date est manquante ou invalide.")
            start_datetime = fields.Datetime.to_string(line.training_date)
            end_datetime = fields.Datetime.from_string(start_datetime) + timedelta(hours=8)
            if line.employee_id:
                # Cherchez le partenaire de l'employé sélectionné
                partner = self.env['res.partner'].search([('employee_ids', '=', line.employee_id.id)], limit=1)
                if not partner:
                    raise ValidationError("L'employé sélectionné n'a pas de partenaire ")
                self.env['calendar.event'].create({
                    'name': 'Formation Odoo',
                    'start_date': start_datetime,
                    'stop_date': end_datetime,
                    'partner_id': partner.id,
                    'attendee_ids': [(4, partner.id)],
                })
            else:
                raise ValidationError("L'employé sélectionné n'existe pas.")
        return res
