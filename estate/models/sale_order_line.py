from odoo import fields, models


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    training_date = fields.Date(string="training date")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    price_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_compute_amount',
                                  currency_field='currency_id')
