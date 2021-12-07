# -*- coding: utf-8 -*-

from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _create_backorder(self):
        picking_ids = self.env['stock.picking']
        for record in self:
            picking_ids |= record
        return picking_ids