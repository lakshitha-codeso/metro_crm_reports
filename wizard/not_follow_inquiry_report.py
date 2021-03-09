# -*- coding: utf-8 -*-

from flectra import api, fields, models


class MetroCRMNotFollowLeadReports(models.TransientModel):
  _name = "metro_crm_reports.notfollowleadreports"
   
  company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
  # date_from = fields.Date(string='Start Date')
  # date_to = fields.Date(string='End Date')
  counselor = fields.Many2one('res.users', string='counselor', index=True)
  stage_id = fields.Many2one('crm.stage', string='Stage', index=True)
  
  def print_report(self):
    data = {
      'model': 'metro_crm_reports.notfollowleadreports',
      'form': self.read()[0]
    }

    return self.env.ref('metro_crm_reports.report_not_follow_lead_list_view_report').report_action(self, data=data)

