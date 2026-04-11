from odoo import _, fields, models
from odoo.exceptions import UserError

class ReturnMedia(models.TransientModel):
    """Retrun Media Wizard"""
    _name = 'return.media'
    _description = 'Media Author'
    media_id = fields.Many2one('op.media', readonly=True)
    media_unit_id = fields.Many2one('op.media.unit', readonly=True, required=True)
    actual_return_date = fields.Date(default=lambda self: fields.Date.today(), required=True)

    def do_return(self):
        for media in self:
            if media.media_unit_id.state and media.media_unit_id.state == 'issue':
                media_move_search = self.env['op.media.movement'].search([('media_unit_id', '=', media.media_unit_id.id), ('state', '=', 'issue')])
                if not media_move_search:
                    raise UserError(_("Can't return media."))
                media_move_search.return_media(media.actual_return_date)
            else:
                raise UserError(_("Media Unit can not be returned because it's already: %s") % dict(media.media_unit_id._fields['state'].selection).get(media.media_unit_id.state))