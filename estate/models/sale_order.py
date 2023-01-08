from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo import api, models, fields


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    approval_state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Approval State', default='pending')
    manager_level = fields.Selection(related='partner_id.manager_level')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
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
        return res

    def action_approve(self):
        for order in self:
            if self.user_has_groups('sales_team.group_sale_manager'):
                order.approval_state = 'approved'
            else:
                raise ValidationError("Only managers can approve sales orders.")