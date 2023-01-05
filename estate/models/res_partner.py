from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    manager_level = fields.Selection([
        ('none', 'Aucun'),
        ('level1', 'Niveau 1'),
        ('level2', 'Niveau 2'),
        ('level3', 'Niveau 3'),
    ], string='Niveau de gestionnaire', default='none')
