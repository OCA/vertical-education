from . import controllers
from . import models
from . import wizard
from . import report
from odoo import api, SUPERUSER_ID

def _openeducat_post_init(env):
    env['publisher_warranty.contract'].update_notification(cron_mode=True)