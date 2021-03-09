# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import time
from flectra.exceptions import UserError
from flectra import models, api, _


class ReportApplicationAnalysis(models.AbstractModel):
    _name = 'report.metro_crm_reports.sms_stu_appl_analaysis_document'



    @api.model
    def get_report_values(self, docids, data=None):
        
        if not data.get('form')['date_from']:
            raise UserError(_("Form content is missing, this report cannot be printed."))
          
        date_from = data.get('form')['date_from'] # date from form
        date_to = data.get('form')['date_to'] # date from form
        course_id = data.get('form')['course_id']
        if course_id:
          addmission_list = self.env['op.admission'].search([('create_date','>',date_from),('create_date','<',date_to),('state','=','done'),('course_id.id','=',course_id[0])],order='create_date asc')
          course_id= course_id[1]
        else:
          course_id= "All"
          addmission_list = self.env['op.admission'].search([('create_date','>',date_from),('create_date','<',date_to),('state','=','done')],order='create_date asc')

        attendence_list =[]
        for app in addmission_list:
          if app.create_date:
            stu_name=""
            if app.name:
              stu_name= app.name
            if app.middle_name:
              stu_name= stu_name+" "+ app.middle_name
            if app.last_name:
              stu_name= stu_name+" "+app.last_name
            vals={
              'name':stu_name,
              'application_no':app.student_id.sequence,
              'phone':app.phone,
              'course':app.course_id.name,
              'enroll_date':app.admission_date,
              'email':app.email,
            }   
            attendence_list.append(vals)
        

        return {
            'data': attendence_list,
            'date_from':date_from,
            'date_to':date_to,
            'get_total_student':len(attendence_list),
            'course_id':course_id,
        }