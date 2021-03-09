from datetime import datetime
from dateutil.relativedelta import relativedelta
from flectra.exceptions import UserError
from flectra import api, models, _

class NotFollowleadrportviewReport(models.AbstractModel):
    _name = 'report.metro_crm_reports.report_no_follow_leadrportview'


    @api.model
    def get_report_values(self, docids, data=None):
        
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
          
        # date_from = data.get('form')['date_from'] # date from form
        # date_to = data.get('form')['date_to'] # date from form
        counselor = data.get('form')['counselor']
        stage_id = data.get('form')['stage_id']
        current_time = datetime.now() - relativedelta(days=1)
        current_time = datetime.strftime(current_time,"%Y-%m-%d %H:%M:%S")

        
        if stage_id and counselor:        
          lead_list = self.env['crm.lead'].search([('type','=','lead'),('create_date','<',current_time),('user_id.id','=',counselor[0]),('stage_id.id','=',stage_id[0]),('probability','!=',0),('probability','!=',100)], order='create_date asc')
          stage_id= stage_id[1]
          counselor= counselor[1]
        elif not stage_id and counselor:        
          lead_list = self.env['crm.lead'].search([('type','=','lead'),('create_date','<',current_time),('user_id.id','=',counselor[0]),('probability','!=',0),('probability','!=',100)], order='create_date asc')
          stage_id= False
          counselor= counselor[1]
        elif stage_id and not counselor:        
          lead_list = self.env['crm.lead'].search([('type','=','lead'),('create_date','<',current_time),('stage_id.id','=',stage_id[0]),('probability','!=',0),('probability','!=',100)], order='create_date asc')
          stage_id= stage_id[1]
          counselor= counselor[1]
        else:
          lead_list = self.env['crm.lead'].search([('type','=','lead'),('create_date','<',current_time),('probability','!=',0),('probability','!=',100)], order='create_date asc')
          stage_id = False


        attendence_list =[]
        for lead in lead_list:
          if lead.create_date:
            vals={
              'name':lead.name,
              'partner':lead.partner_id.name,
              'create_date':lead.create_date,
              'source':lead.source_id.name,
              'email_from':lead.email_from,
              'phone':lead.phone,
              'counselor':lead.user_id.name,
              'course':lead.application_id.course_id.name,
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
            
        }
   