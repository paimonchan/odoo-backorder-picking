# -*- coding: utf-8 -*-

from odoo import models, api

class StockPicking(models.Model):
    """
    NOTE: merge backorder can be disable by set this parameter `paimon.disable_merge_backorder`
    follow this instruction to disable merge backorder:
    1. go to technical mode in menu setting (as developer mode)
    2. go to menu tecknical -> system parameter
    3. create new entry with 
       - key                : paimon.disable_merge_backorde
       - value              : True
    """

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
        """
        override function create, set printed to true so product qty not merge into existing qty
        """
        record = super().create(vals)
        param = self.env['ir.config_parameter'].sudo()
        disable_merge_backorder = param.get_param('paimon.disable_merge_backorder')
        if not disable_merge_backorder:
            record.write(dict(printed=True))
        return record