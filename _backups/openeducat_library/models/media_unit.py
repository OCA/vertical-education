from odoo import api, fields, models

class OpMediaUnit(models.Model):
    _name = 'op.media.unit'
    _inherit = 'mail.thread'
    _description = 'Media Unit'
    _order = 'name'
    name = fields.Char(required=True)
    media_id = fields.Many2one('op.media', required=True, tracking=True)
    barcode = fields.Char(size=20)
    movement_lines = fields.One2many('op.media.movement', 'media_unit_id', 'Movements')
    state = fields.Selection([('available', 'Available'), ('issue', 'Issued')], default='available', tracking=True)
    media_type_id = fields.Many2one(related='media_id.media_type_id', store=True)
    active = fields.Boolean(default=True)
    _sql_constraints = [('unique_name_barcode', 'unique(barcode)', 'Barcode must be unique per Media unit!')]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            x = self.env['ir.sequence'].next_by_code('op.media.unit') or '/'
            vals['barcode'] = x
        return super().create(vals_list)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search([('barcode', operator, name)] + args, limit=limit)
        return [(res.id, res.display_name) for res in recs]