from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manager_level = fields.Selection(related='partner_id.manager_level')

    # Surcharge de la méthode action_confirm pour créer un événement dans le calendrier de l'employé sélectionné
    def action_confirm(self):
        # Appel de la méthode originale
        res = super(SaleOrder, self).action_confirm()
        # Parcours de toutes les lignes de commande de la commande de vente
        for line in self.order_line:
            # Si une date de formation et un employé sont sélectionnés pour la ligne de commande
            if line.training_date and line.employee_id:
                # Récupération de l'adresse du domicile de l'employé
                employee_home_address = line.employee_id.address_home_id
                # Création de l'événement dans le calendrier de l'employé
                self.env['calendar.event'].create({
                    'name': 'Formation Odoo',
                    'start_date': line.training_date,
                    'stop_date': line.training_date,
                    'partner_ids': [(4, employee_home_address.id)],
                })
        # Renvoi du résultat de la méthode originale
        return res
