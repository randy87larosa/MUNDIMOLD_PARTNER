# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Project Template & Predecessors",
    'summary': """Adds function to copy of milestones when creating
                  a project from template""",
    'author': "Patrick Wilson, Odoo Community Association (OCA)",
    'website': "https://github.com/OCA/project",
    'category': 'Project Management',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'project_template',
        'project_native',
        ],
    'application': False,
    'auto_install': True,
    'maintainers': ['indaws'],
}
