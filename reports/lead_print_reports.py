from datetime import datetime
from dateutil.relativedelta import relativedelta
from flectra.exceptions import UserError
from flectra import api, models, _

class leadrportviewReport(models.AbstractModel):
    _name = 'report.metro_crm_reports.report_leadrportview'


    @api.model
    def get_report_values(self, docids, data=None):
        
        if not data.get('form')['date_from']:
            raise UserError(_("Form content is missing, this report cannot be printed."))
          
        date_from = data.get('form')['date_from'] # date from form
        date_to = data.get('form')['date_to'] # date from form
        
        lead_list = self.env['crm.lead'].search([('type','=','lead'),('create_date','>',date_from),('create_date','<',date_to)],order='create_date asc')
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
   