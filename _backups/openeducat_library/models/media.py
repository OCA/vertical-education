from odoo import fields, models

class OpMedia(models.Model):
    _name = 'op.media'
    _description = 'Media Details'
    _inherit = 'mail.thread'
    _order = 'name'
    name = fields.Char('Title', size=128, required=True)
    isbn = fields.Char('ISBN Code', size=64)
    tags = fields.Many2many('op.tag', string='Tag(s)')
    author_ids = fields.Many2many('op.author', string='Author(s)', required=True)
    edition = fields.Char()
    description = fields.Text()
    publisher_ids = fields.Many2many('op.publisher', string='Publisher(s)', required=True)
    course_ids = fields.Many2many('op.course')
    movement_line = fields.One2many('op.media.movement', 'media_id', 'Movements')
    subject_ids = fields.Many2many('op.subject')
    internal_code = fields.Char(size=64)
    queue_ids = fields.One2many('op.media.queue', 'media_id', 'Media Queue')
    unit_ids = fields.One2many('op.media.unit', 'media_id', 'Units')
    media_type_id = fields.Many2one('op.media.type')
    active = fields.Boolean(default=True)
    _sql_constraints = [('unique_name_isbn', 'unique(isbn)', 'ISBN code must be unique per media!'), ('unique_name_internal_code', 'unique(internal_code)', 'Internal Code must be unique per media!')]