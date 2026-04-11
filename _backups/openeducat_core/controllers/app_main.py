import werkzeug.utils
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.web import Home as home

class OpeneducatHome(home):

    @http.route()
    def web_login(self, redirect=None, **kw):
        response = super().web_login(redirect=redirect, **kw)
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group('base.group_user'):
                redirect = '/web?' + request.httprequest.query_string.decode('utf-8')
            elif request.env.user.is_parent:
                redirect = '/my/child'
            else:
                redirect = '/my'
            return werkzeug.utils.redirect(redirect)
        return response

    def _login_redirect(self, uid, redirect=None):
        if redirect:
            return super()._login_redirect(uid, redirect)
        if request.env.user.is_parent:
            return '/my/child'
        return '/my'