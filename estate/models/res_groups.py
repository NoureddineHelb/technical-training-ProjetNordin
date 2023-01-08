from odoo import fields, models

class ResGroups(models.Model):
    _inherit = 'res.groups'

    user_type = fields.Selection(
        [('admin', 'Admin'), ('manager_1', 'Manager Level 1'), ('manager_2', 'Manager Level 2'),
         ('manager_3', 'Manager Level 3'), ('partner', 'Partner')],
        string='User Type',
        required=True,
        default='partner'
    )
