
# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.


from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from flectra import api, fields, models, tools, SUPERUSER_ID
from flectra.tools.translate import _
from flectra.tools import email_re, email_split
from flectra.exceptions import UserError, AccessError

class Admsn(models.Model):
  _inherit = 'op.admission'
  
  crm_lead_id = fields.Many2one('crm.lead', string="CRM")
  # attachment = fields.Many2many('ir.attachment', 'attach_rel', 'doc_id','attach_id3',               				
  #                                       string="Attachment",                                           				
  #                       help='You can attach the copy of your document', copy=False)
  

  
class Lead(models.Model):
  _inherit = "crm.lead"


  company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=False, relation="res.currency")
  initial_payment  = fields.Float('Initial Payment ', default=0.00)
  balance_payment  = fields.Float('Balance Payment ', compute="get_balance_payment_value", readonly=True)
  application_id = fields.One2many('op.admission','crm_lead_id', string="Application")
  



  @api.multi
  @api.depends('planned_revenue','initial_payment')
  def get_balance_payment_value(self):
    for rec in self:
      if rec.planned_revenue:
        rec.balance_payment = rec.planned_revenue - rec.initial_payment
  

  def action_email_send_opertunity(self):
    '''
      This function opens a window to compose an email, with the edi sale template message loaded by default
    '''
    self.ensure_one()
    ir_model_data = self.env['ir.model.data']
    try:
      template_id = ir_model_data.get_object_reference('metro_crm_module', 'email_template_edi_oppertunity')[1]
    except ValueError:
      template_id = False
    try:
      compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
    except ValueError:
      compose_form_id = False
    ctx = {
      'default_model': 'crm.lead',
      'default_res_id': self.ids[0],
      'default_use_template': bool(template_id),
      'default_template_id': template_id,
      'default_composition_mode': 'comment',
      'mark_so_as_sent': True,
      'custom_layout': "sale.mail_template_data_notification_email_sale_order",
      'proforma': self.env.context.get('proforma', False),
      'force_email': True
    }
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
    

# class Attachment(models.Model):
#     _inherit = 'ir.attachment'
#         attach_rel = fields.Many2many('res.partner', 'attachment', 'attachment_id3', 'document_id',string="Attachment", invisible=1 )