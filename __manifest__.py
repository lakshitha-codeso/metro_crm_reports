# -*- coding: utf-8 -*-
{
    'name': "metro crm reports",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','openeducat_timetable','openeducat_admission'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/report_header_layout_internal.xml',
        'reports/lead_print_reports.xml',
        'reports/report_menu.xml',
        'reports/pipline_print_by_counselor.xml',
        'reports/no_follow_report_view.xml',
        'reports/report_crm_lead_by_courses.xml',
        'reports/crm_total_enroll_rport.xml',
        'reports/sms_student_outstanding_payments.xml',

        #sms
        'reports/sms_studen_addmission_report.xml',
        'reports/sms_studen_timetable_report.xml',
        'reports/sms_studen_payment_report.xml',
        'views/templates.xml',


        'wizard/lead_report_generate.xml',
        'wizard/lead_report_generate_by_counsiller.xml',
        'wizard/not_follow_inquiry_report.xml',
        'wizard/filter_pipeline_by_programe.xml',
        'wizard/crm_total_enroll_pipline_report.xml',
        #sms
        'wizard/sms_stu_application_wizard.xml',
        'wizard/sms_stu_timetable_wizard.xml',
        'wizard/sms_stu_payments_wizard.xml',
        # 'wizard/sms_stu_timetable__coursewizard.xml',

        'data/mail_template_data.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True
}