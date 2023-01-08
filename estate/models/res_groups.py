from odoo import fields, models

class ResGroups(models.Model):
    _inherit = 'res.groups'

    user_type = fields.Selection(
        [('admin', 'Admin'), ('manager', 'Manager'), ('partner', 'Partner')],
        string='User Type',
        required=True,
        default='partner'
    )
