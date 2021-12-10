# -*- coding: utf-8 -*-

from odoo import models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _create_backorder(self):
        """
        overwrite function _create_backorder.
        this function is called to create new stock picking on remaining backorder item.
        to prevent create new stock picking, return original (source) picking so the remaining backorder item,
        will be put in the same picking as source picking.
        """
        param = self.env['ir.config_parameter'].sudo()
        disable_merge_backorder = param.get_param('paimon.disable_merge_backorder')
        if disable_merge_backorder:
            return super()._create_backorder()
        picking_ids = self.env['stock.picking']
        for record in self:
            picking_ids |= record
        return picking_ids

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.write(dict(printed=True))
        return record