# -*- coding: utf-8 -*-

from flectra import api, fields, models


class MetroSMSStuAdmissionreport(models.TransientModel):
  _name = "metro_crm_reports.smsstuadmissionwizard"
   
  #company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
  date_from = fields.Date(string='Start Date Enrollment', required=True)
  date_to = fields.Date(string='End Date Enrollment' , required=True)
  course_id = fields.Many2one('op.course', 'Course')
  
  def print_report(self):
    data = {
      'model': 'metro_crm_reports.smsstuadmissionwizard',
      'form': self.read()[0]
    }

    return self.env.ref('metro_crm_reports.sms_stu_appl_analaysis_menu').report_action(self, data=data)

