from odoo import fields, models


class Employee(models.Model):
    _inherit = 'hr.employee'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
