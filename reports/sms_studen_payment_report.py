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


class ReportSMSPaymenteAnalysis(models.AbstractModel):
    _name = 'report.metro_crm_reports.sms_stu_payment_document'

    # @api.model
    # def get_student_name(self, student_id):
    #     student_id = self.env['op.student'].search([('id','=',student_id)])
    #     students=[]
    #     for stu in student_id:
    #         vals={
    #             'name':stu.name,
    #             'phone':stu.phone,
    #             'number':stu.sequence,
    #         }
    #         students.append(vals)
    #     return students
    @api.model
    def get_invoice_details(self,pay):
        if pay.invoice_id:
            account= self.env['account.invoice'].search([('id','=',pay.invoice_id.id),('state','=','paid')])
            amount=0.00
            if account:            
                for inv in account:
                    amount += inv.amount_total - inv.residual
            return amount
        else:
            amount= "None"
            return amount
    
    @api.model
    def get_paid_details(self,pay):
        amount=0.00
        if pay.invoice_id:
            account= self.env['account.invoice'].search([('id','=',pay.invoice_id.id)])
            amount=0.00
            for inv in account:
                if inv.state=="paid":
                    amount += inv.amount_total - inv.residual
            return amount
        else:
            
            return amount

    @api.model
    def get_report_values(self, docids, data=None):
        
        # if not data.get('form')['date_from']:
        #     raise UserError(_("Form content is missing, this report cannot be printed."))

        student_id = data.get('form')['student_id'] # date from form 
        # date_from = data.get('form')['date_from'] # date from form
        # date_to = data.get('form')['date_to'] # date from form
        payments_data=[]
        stu_name=student_id[1]
        stu_contact=""
        total_amount = 0.00
        paid_amount = 0.00
        payments=  self.env['op.student.fees.details'].search([('student_id.id','=',student_id[0])])
        for pay in payments:
            stu_name= pay.student_id.name+" "+ pay.student_id.last_name
            stu_contact = pay.student_id.phone
            total_amount += pay.amount
            p_amount = self.get_paid_details(pay)
            paid_amount += p_amount
            payment_val={
                'date':pay.date,
                'amount':round(pay.amount,2),
                'paid':self.get_invoice_details(pay),
                
            }
            payments_data.append(payment_val)
        due_payments = round(total_amount,2)-round(paid_amount,2)
        return {
            'student_name':stu_name,
            'phone':stu_contact,
            'total_amount':round(total_amount,2),
            'paid_amount':round(paid_amount,2),
            'due_amount':due_payments,
            'data': payments_data,
        }

        # if student_id:
        #     batch_course_id = self.env['op.student.course'].search([('student_id.id','=',student_id[0])])
        #     # student_data=[]
            
        #     batch_and_course=[] #batch Course vals
        #     for bc in batch_course_id:
        #         timetable_data=[]#timtable vals
               
        #         timetable_ids = self.env['op.session'].search([('course_id.id','=',bc.course_id.id),('batch_id.id','=',bc.batch_id.id),('start_datetime','>',date_from),('end_datetime','<',date_to)])
                
        #         for time in timetable_ids:
        #             time_vals={ #timtable vals
        #                 'subject':time.subject_id.name,
        #                 'classroom':time.classroom_id.name,
        #                 'start_time':time.start_datetime,
        #                 'duration':time.timing_id.duration,
        #             }
        #             timetable_data.append(time_vals)
        #         bc_vals={   #batch Course vals
        #             'batch':bc.batch_id.name,
        #             'course':bc.course_id.name,
        #             'timetable':timetable_data,
        #         }
        #         batch_and_course.append(bc_vals)
        #     student_id=student_id[0]
            # return {
            #     'student_name':self.get_student_name(student_id),
            #     'data': batch_and_course,
            #     'date_from':date_from,
            #     'date_to':date_to
            # }

        
        