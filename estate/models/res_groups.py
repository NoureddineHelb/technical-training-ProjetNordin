from odoo import models, fields

class ResGroups(models.Model):
    _name = 'res.groups'
    _inherit = 'res.groups'

    approval_level = fields.Selection([
        ('none', 'None'),
        ('level1', 'Level 1'),
        ('level2', 'Level 2'),
        ('level3', 'Level 3'),
    ], string='Approval Level', default='none')
