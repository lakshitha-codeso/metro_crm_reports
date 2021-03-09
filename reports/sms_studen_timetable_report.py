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


class ReportSMSTimetableAnalysis(models.AbstractModel):
    _name = 'report.metro_crm_reports.sms_stu_timetable_document'

    @api.model
    def get_student_name(self, student_id):
        student_id = self.env['op.student'].search([('id','=',student_id)])
        students=[]
        for stu in student_id:
            vals={
                'name':stu.name,
                'phone':stu.phone,
                'number':stu.sequence,
            }
            students.append(vals)
        return students

    @api.model
    def get_report_values(self, docids, data=None):
        
        if not data.get('form')['date_from']:
            raise UserError(_("Form content is missing, this report cannot be printed."))

        student_id = data.get('form')['student_id'] # date from form 
        date_from = data.get('form')['date_from'] # date from form
        date_to = data.get('form')['date_to'] # date from form
        
        if student_id:
            batch_course_id = self.env['op.student.course'].search([('student_id.id','=',student_id[0])])
            # student_data=[]
            
            batch_and_course=[] #batch Course vals
            for bc in batch_course_id:
                timetable_data=[]#timtable vals
               
                timetable_ids = self.env['op.session'].search([('course_id.id','=',bc.course_id.id),('batch_id.id','=',bc.batch_id.id),('start_datetime','>',date_from),('end_datetime','<',date_to)])
                
                for time in timetable_ids:
                    time_vals={ #timtable vals
                        'subject':time.subject_id.name,
                        'classroom':time.classroom_id.name,
                        'start_time':time.start_datetime,
                        'duration':time.timing_id.duration,
                    }
                    timetable_data.append(time_vals)
                bc_vals={   #batch Course vals
                    'batch':bc.batch_id.name,
                    'course':bc.course_id.name,
                    'timetable':timetable_data,
                }
                batch_and_course.append(bc_vals)
            student_id=student_id[0]
            return {
                'student_name':self.get_student_name(student_id),
                'data': batch_and_course,
                'date_from':date_from,
                'date_to':date_to
            }

        
        