# -*- coding: utf-8 -*-

from flectra import api, fields, models


class MetroSMSStuPaymentreport(models.TransientModel):
    _name = "metro_crm_reports.smsstupaymentwizard"
   
    #company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    
    student_id= fields.Many2one('op.student', 'Student')
    report_type = fields.Selection([('total','Total Fees'),('outstanding','Out Standing Fees')],string="Report", required=True, default="total")
   
    # date_from = fields.Date(string='Start Date ', required=True)
    # date_to = fields.Date(string='End Date ' , required=True)
  

    # @api.onchange('student_id')
    # def onchange_course(self):
    #     if self.student_id:
    #         self.course_id=self.student_id.course_detail_ids.course_id
        


    def print_report(self):
        data = {
        'model': 'metro_crm_reports.smsstupaymentwizard',
        'form': self.read()[0]
        }
        datas = self.read(['student_id', 'report_type'])[0]
        if datas['report_type']=="total":
            return self.env.ref('metro_crm_reports.sms_stu_payment_reportmenu').report_action(self, data=data)
        else:
            return self.env.ref('metro_crm_reports.sms_stu_outstandpayment_reportmenu').report_action(self, data=data)

