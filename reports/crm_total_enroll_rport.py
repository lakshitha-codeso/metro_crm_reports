from datetime import datetime
from dateutil.relativedelta import relativedelta
from flectra.exceptions import UserError
from flectra import api, models, _

class leadrportviewReportBycounsellor(models.AbstractModel):
    _name = 'report.metro_crm_reports.report_crm_total_enroll_report'


    @api.model
    def get_report_values(self, docids, data=None):
        
        if not data.get('form')['date_from']:
            raise UserError(_("Form content is missing, this report cannot be printed."))
          
        date_from = data.get('form')['date_from'] # date from form
        date_to = data.get('form')['date_to'] # date from form
        # counselor = data.get('form')['counselor']
        # if stage_id:        
        #   lead_list = self.env['crm.lead'].search([('type','=','opportunity'),('create_date','>',date_from),('create_date','<',date_to),('probability','=',100)], order='create_date asc')
        #   stage_id= stage_id[1]
        # else:
        lead_list = self.env['crm.lead'].search([('type','=','opportunity'),('create_date','>',date_from),('create_date','<',date_to),('probability','=',100)], order='create_date asc')
        
        attendence_list =[]
        for lead in lead_list:
          if lead.create_date:
            vals={
              'name':lead.name,
              'contact':lead.phone,
              'partner':lead.partner_id.name,
              'email_from':lead.email_from,
              'en_date':lead.application_id.admission_date,
              'course':lead.application_id.course_id.name,
              'level':lead.application_id.course_id.evaluation_type,
              'tot_value':lead.planned_revenue,
              'in_value':lead.initial_payment,
        
             
            }   
            attendence_list.append(vals)
        
        
           
        # date_period=[]
        # datess ={
        #     'req_start_date':date_from,
        #     'req_end_date':date_to,
        # }
        # date_period.append(datess)
        return {
            'data': attendence_list,
            'date_from':date_from,
            'date_to':date_to,
        }
   