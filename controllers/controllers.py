# -*- coding: utf-8 -*-
from flectra import http

# class MetroCrmReports(http.Controller):
#     @http.route('/metro_crm_reports/metro_crm_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/metro_crm_reports/metro_crm_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('metro_crm_reports.listing', {
#             'root': '/metro_crm_reports/metro_crm_reports',
#             'objects': http.request.env['metro_crm_reports.metro_crm_reports'].search([]),
#         })

#     @http.route('/metro_crm_reports/metro_crm_reports/objects/<model("metro_crm_reports.metro_crm_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('metro_crm_reports.object', {
#             'object': obj
#         })