{
    'name': 'Project Task SubTask Checklist',
    'version': '1.2.3',
    'author': 'FreelancerApps',
    'category': 'Project',
    'summary': 'Project CheckList SubTask Checklist Project SubTask CRM Check List Project Checklist Employee crm_checklist Sale Order CheckList construction checklist Read Only User Hide Any Menu multi level approve website document attachment product attachment',
    'depends': ['base', 'project', 'web_kanban_gauge'],
    'description': '''
Added CheckList And CheckList Related Features Into Project
-----------------------------------------------------------
With the help of this module you can divide task or sub task into list of activities, so task and subtask will easily control in Odoo project management

Key features:
-------------
* Any Number Of Configurable Checklist(General or Project Specific)
* Configurable Checklist Stages(Default 3 Stages you can add more stages).
* Only Admin And Manager Can Add Remove Checklist.
* Any Number Of Checklist Activities.
* Set Color Depend Checklist Activity Stage.
* Separate Checklist Activity Menu For Different Filter Group By Options.
* Bulk Approve / Cancel CheckList activity.
* Check list Progress In Task Kanban And Form View.
* Activities Can Checked From Project Kanban And Form View.
* Restrict Task Completion Before All Checklist Either Canceled Or Completed.

<Search Keyword for internal user only>
---------------------------------------
Project Task SubTask Checklist Project Task SubTask Project Task Checklist Project SubTask Task Project SubTask Checklist Task Project SubTask Project Checklist Task Project Checklist SubTask Task Project Checklist Task SubTask Project SubTask Task Checklist SubTask Project Task Project Checklist 

CRM Check List and Approval Process Project Checklist Employee Entry Exit Checklist Checklist for Lead and Opportunity crm_checklist Sale Order Approval Check Lists
construction project construction checklist generate barcode product auto Restrict Read Only User Hide Any Menu Restrict User Menus multi level approve three level approve Tripple Approve Purchase Tripple Approval Project Checklist Task Checklist
website document attachment product attachment
    ''',
    'data': [
        'security/checklist_security.xml',
        'security/ir.model.access.csv',
        'views/res_config_view.xml',
        'views/views.xml',
        'data/checklist_data.xml',
        'wizard/activity_approve_reject_view.xml',
    ],
    'images': ['static/description/task_checklist_banner.png'],
    'price': 14.99,
    'currency': 'USD',
    'license': 'OPL-1',
    'application': True,
    'installable': True,
    'auto_install': False,
}
