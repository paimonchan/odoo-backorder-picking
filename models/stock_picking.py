# -*- coding: utf-8 -*-

from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _create_backorder(self):
        param = self.env['ir.config_parameter'].sudo()
        disable_merge_backorder = param.get_param('paimon.disable_merge_backorder')
        if disable_merge_backorder:
            return super()._create_backorder()
        picking_ids = self.env['stock.picking']
        for record in self:
            picking_ids |= record
        return picking_ids