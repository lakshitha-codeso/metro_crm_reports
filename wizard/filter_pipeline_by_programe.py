# -*- coding: utf-8 -*-

from flectra import api, fields, models


class MetroCRMLeadReportsbyCourse(models.TransientModel):
  _name = "metro_crm_reports.leadreportsbycourses"
   
  company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
  date_from = fields.Date(string='Start Date', required=True)
  date_to = fields.Date(string='End Date', required=True)
  course_id = fields.Many2one('op.course', 'Course', )
  
  def print_report(self):
    data = {
      'model': 'metro_crm_reports.leadreportsbycourses',
      'form': self.read()[0]
    }

    return self.env.ref('metro_crm_reports.report_lead_filter_by_courseslist_view_report').report_action(self, data=data)

