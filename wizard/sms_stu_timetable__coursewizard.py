# -*- coding: utf-8 -*-

from flectra import api, fields, models


class MetroSMSStuTimtablecourcereport(models.TransientModel):
    _name = "metro_crm_reports.smsstutimetablecourcewizard"
   
    #company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    
    cource_id= fields.Many2one('op.course', 'Course', required=True)
    batch_id= fields.Many2one('op.batch', 'Batch', required=True)
    # course_id = fields.Many2one('op.course', 'Course' )
   
    date_from = fields.Datetime(string='Start Date ', required=True)
    date_to = fields.Datetime(string='End Date ' , required=True)
  

    # @api.onchange('student_id')
    # def onchange_course(self):
    #     if self.student_id:
    #         self.course_id=self.student_id.course_detail_ids.course_id
        
    @api.multi
    @api.onchange('cource_id')
    def _select_batchfrom_cources(self):
        result = {}
        if self.cource_id: 
            domain = [('course_id','=',self.cource_id.id)]
            result['domain'] = {'batch_id':domain}            
        return result

    def print_report(self):
        data = {
        'model': 'metro_crm_reports.smsstutimetablecourcewizard',
        'form': self.read()[0]
        }

        return self.env.ref('metro_crm_reports.sms_stu_timetable_courcereportmenu').report_action(self, data=data)

