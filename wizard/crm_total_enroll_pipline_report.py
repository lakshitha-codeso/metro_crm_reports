# -*- coding: utf-8 -*-

from flectra import api, fields, models


class MetroCRMTotalEnroll(models.TransientModel):
  _name = "metro_crm_reports.crmtotalenrollwizard"
   
  #company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
  date_from = fields.Date(string='Start Date ', required=True)
  date_to = fields.Date(string='End Date ' , required=True)
  
  def print_report(self):
    data = {
      'model': 'metro_crm_reports.crmtotalenrollwizard',
      'form': self.read()[0]
    }

    return self.env.ref('metro_crm_reports.crm_total_enroll_report_menu').report_action(self, data=data)

