from odoo import fields, models


class CalendarAttendee(models.Model):
    _name = 'calendar.attendee'
    _description = 'Calendar Attendee'

    # Définition du champ "Attendee" (partenaire) comme obligatoire
    partner_id = fields.Many2one('res.partner', required=True, string='Attendee')
    # Autres champs du modèle...
