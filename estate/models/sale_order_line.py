from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Date(string="training date")
    employee_id = fields.Many2one('hr.employee', string="Employee")

    def create(self, values):
        line = super(SaleOrderLine, self).create(values)
        if line.employee_id and line.training_date:
            start_datetime = fields.Datetime.to_string(line.training_date)
            end_datetime = fields.Datetime.from_string(start_datetime) + timedelta(hours=8)
            partner = self.env['res.partner'].search([('name', '=', line.employee_id.name)], limit=1)
            if not partner:
                raise ValidationError("L'employé sélectionné n'a pas de partenaire ")
            self.env['calendar.event'].create({
                'name': 'Formation Odoo',
                'start_date': start_datetime,
                'stop_date': end_datetime,
                'partner_id': partner.id,
                'attendee_ids': [(4, partner.id)],
            })
        return line