# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from flectra import api, fields, models, tools, SUPERUSER_ID
from flectra.tools.translate import _
from flectra.tools import email_re, email_split
from flectra.exceptions import UserError, AccessError, ValidationError


# class metro_crm_reports(models.Model):
#     _name = 'metro_crm_reports.metro_crm_reports'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100



class OpSession(models.Model):
  _inherit = 'op.session'


  cus_edited= fields.Boolean("Edited")

  all_emails = fields.Char("emails")

  @api.multi
  def write (self, vals):
      self.ensure_one()
      if 'state' not in vals.keys() and 'cus_edited' not in vals.keys() and 'all_emails' not in vals.keys() :
          self.cus_edited = True
      res = super(OpSession, self).write(vals)
      return res


  def send_timetable_updateemail(self):
    self.ensure_one()
    ir_model_data = self.env['ir.model.data']

    if self.course_id:
        timetabale= self.env['op.student.course'].search([('course_id.id','=',self.course_id.id),('batch_id.id','=',self.batch_id.id)])
        emails=""
        print("ssssssssssauuuuuiuiuiuiui",timetabale)
        if timetabale:
            for em in timetabale:
                if em.student_id.partner_id.email:
                    emails= emails+ "," +em.student_id.partner_id.email
                    print("ssssssssssauuuuuiuiuiuiui",em.student_id.partner_id.email)
                    print("ssssssssssauuuuuiuiuiuiui",em.student_id.email)
        self.write({'all_emails':emails})
        # self.all_emails = emails
    else:
        print("ssssssssssauuuuuiuiuiuiui")
    try:
      template_id = ir_model_data.get_object_reference('metro_crm_reports', 'email_template_for_send_all_mail')[1]
    except ValueError:
      template_id = False
    try:
      compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
    except ValueError:
      compose_form_id = False
    ctx = {
      'default_model': 'op.session',
      'default_res_id': self.ids[0],
      'default_use_template': bool(template_id),
      'default_template_id': template_id,
      'default_composition_mode': 'comment',
      'mark_so_as_sent': True,
      'custom_layout': "sale.mail_template_data_notification_email_sale_order",
      'proforma': self.env.context.get('proforma', False),
      'force_email': True
    }
    self.write({'cus_edited':False})
    return {
      'type': 'ir.actions.act_window',
      'view_type': 'form',
      'view_mode': 'form',
      'res_model': 'mail.compose.message',
      'views': [(compose_form_id, 'form')],
      'view_id': compose_form_id,
      'target': 'new',
      'context': ctx,
    }

class OpAdmission(models.Model):
  _inherit = 'op.admission'




  @api.multi
  def enroll_student_cus(self):
    for record in self:
      total_admission = self.env['op.admission'].search_count(
          [('register_id', '=', record.register_id.id),
           ('state', '=', 'done')])
      if record.register_id.max_count:
          if not total_admission < record.register_id.max_count:
              msg = 'Max Admission In Admission Register :- (%s)' % (
                  record.register_id.max_count)
              raise ValidationError(_(msg))
      if not record.student_id:
          vals = record.get_student_vals()
          vals.update({'partner_id': record.partner_id.id})
          student_id = self.env['op.student'].create(vals).id
      else:
          student_id = record.student_id.id
          record.student_id.write({
              'course_detail_ids': [[0, False, {
                  'course_id':
                  record.course_id and record.course_id.id or False,
                  'batch_id':
                  record.batch_id and record.batch_id.id or False,
              }]],
          })
      if record.fees_term_id:
            val = []
            product_id = record.register_id.product_id.id
            for line in record.fees_term_id.line_ids:
                no_days = line.due_days
                per_amount = line.value
                amount = (per_amount * record.fees) / 100
                ad_date = datetime.strptime(record.admission_date, "%Y-%m-%d")
                date = (
                    ad_date + relativedelta(days=no_days)).date()
                dict_val = {
                    'fees_line_id': line.id,
                    'amount': amount,
                    'date': date,
                    'product_id': product_id,
                    'state': 'draft',
                }
                val.append([0, False, dict_val])
            self.env['op.student'].browse(student_id).write({
                'fees_detail_ids': val
            })
      record.write({
          'nbr': 1,
          'state': 'done',
          # 'admission_date': fields.Date.today(),
          'student_id': student_id,
      })
      reg_id = self.env['op.subject.registration'].create({
          'student_id': student_id,
          'batch_id': record.batch_id.id,
          'course_id': record.course_id.id,
          'min_unit_load': record.course_id.min_unit_load or 0.0,
          'max_unit_load': record.course_id.max_unit_load or 0.0,
          'state': 'draft',
      })
      reg_id.get_subjects()

