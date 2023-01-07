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
            if line.training_date and line.employee_id:
                # Créez un partenaire pour l'employé sélectionné
                partner = self.env['res.partner'].create({'name': line.employee_id.name})
                # Affectez le partenaire à l'employé sélectionné
                line.employee_id.partner_id = partner
                self.env['calendar.event'].create({
                    'name': 'Formation Odoo',
                    'start_date': start_datetime,
                    'stop_date': end_datetime,
                    'partner_id': partner.id,
                    'attendee_ids': [(4, partner.id)],
                })
        return res