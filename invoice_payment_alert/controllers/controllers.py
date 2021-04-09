# -*- coding: utf-8 -*-
# from odoo import http


# class TestAlert(http.Controller):
#     @http.route('/test_alert/test_alert/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_alert/test_alert/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_alert.listing', {
#             'root': '/test_alert/test_alert',
#             'objects': http.request.env['test_alert.test_alert'].search([]),
#         })

#     @http.route('/test_alert/test_alert/objects/<model("test_alert.test_alert"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_alert.object', {
#             'object': obj
#         })
