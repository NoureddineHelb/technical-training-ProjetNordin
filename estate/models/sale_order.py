from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manager_level = fields.Selection(related='partner_id.manager_level')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            if line.training_date and line.employee_id:
                self.env['calendar.event'].create({
                    'name': 'Formation Odoo',
                    'start_date': line.training_date,
                    'stop_date': line.training_date,
                    'partner_id': line.employee_id.partner_id.id,
                })
        return res
