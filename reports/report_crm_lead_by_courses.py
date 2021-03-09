from datetime import datetime
from dateutil.relativedelta import relativedelta
from flectra.exceptions import UserError
from flectra import api, models, _

class NotFollowleadrportviewReportBycourses(models.AbstractModel):
    _name = 'report.metro_crm_reports.report_leadr_by_courses_portview'


    @api.model
    def get_report_values(self, docids, data=None):
        
        if not data.get('form')['date_from']:
            raise UserError(_("Form content is missing, this report cannot be printed."))
          
        date_from = data.get('form')['date_from'] # date from form
        date_to = data.get('form')['date_to'] # date from form
        course_id = data.get('form')['course_id']
        if course_id:
          lead_list = self.env['crm.lead'].search([('type','=','opportunity'),('create_date','>',date_from),('create_date','<',date_to),('application_id.course_id.id','=',course_id[0])],order='create_date asc')
        else:
          lead_list = self.env['crm.lead'].search([('type','=','opportunity'),('create_date','>',date_from),('create_date','<',date_to)],order='create_date asc')

        attendence_list =[]
        for lead in lead_list:
          if lead.create_date:
            # admision =self.env['op.admission'].search([('crm_lead_id','=',lead.id),('course_id.id','=',course_id[0])])
            # Courses="s"
            # for rec in admision:
            #   Courses=Courses + rec.course_id.name

            vals={
              'name':lead.name,
              'create_date':lead.create_date,
              'partner':lead.partner_id.name,
              'source':lead.source_id.name,
              'course':lead.application_id.course_id.name,
              'email_from':lead.email_from,
              'phone':lead.phone,
              'stage':lead.stage_id.name,
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
   