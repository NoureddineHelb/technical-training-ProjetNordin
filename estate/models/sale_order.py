from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manager_level = fields.Selection(related='partner_id.manager_level')
    calendar_event_id = fields.Many2one('hr.employee', comodel_name='calendar.event', string='Calendar Event')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            if line.training_date and line.employee_id:
                employee = line.employee_id
                event = self.env['calendar.event'].create({
                    'name': 'Formation Odoo!',
                    'start_date': line.training_date,
                    'stop_date': line.training_date,
                    'partner_ids': [(4, employee.id)],
                })
                employee.write({
                    'calendar_event_id': event.id,
                })
        return res
