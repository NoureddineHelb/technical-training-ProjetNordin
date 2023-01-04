from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    is_employee = fields.Boolean(string="Is employee", default=True)
