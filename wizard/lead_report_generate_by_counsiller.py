# -*- coding: utf-8 -*-

from flectra import api, fields, models


class MetroCRMLeadReportscounselor(models.TransientModel):
  _name = "metro_crm_reports.leadreportsbycounselor"
   
  company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
  date_from = fields.Date(string='Start Date', required=True)
  date_to = fields.Date(string='End Date', required=True)
  counselor = fields.Many2one('res.users', string='counselor', index=True, default=lambda self: self.env.user, required=True)
  stage_id = fields.Many2one('crm.stage', string='Stage', index=True)
  def print_report(self):
    data = {
      'model': 'metro_crm_reports.leadreportsbycounselor',
      'form': self.read()[0]
    }

    return self.env.ref('metro_crm_reports.report_lead_list_view_by_counselor_report').report_action(self, data=data)

