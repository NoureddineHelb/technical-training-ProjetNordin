from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    employee_ids = fields.One2many(comodel_name='hr.employee', inverse_name='partner_id', string='Employees')
    manager_level = fields.Selection([
        ('none', 'Aucun'),
        ('level1', 'Niveau 1'),
        ('level2', 'Niveau 2'),
        ('level3', 'Niveau 3'),
    ], string='Niveau de gestionnaire', default='none')
    max_order_amount = fields.Float(string='Montant maximum de commande')
