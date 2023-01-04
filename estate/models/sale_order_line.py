from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Date(string="training date")
    employee_id = fields.Many2one('hr.employee', string="Employee")