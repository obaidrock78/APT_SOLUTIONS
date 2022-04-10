import dataclasses
from functools import reduce

from typing import Optional

@dataclasses.dataclass(frozen=True)
class AppPermission:
    slug: str
    title: str
    desc: str

    def __repr__(self):
        return "<AppPermission: \'%s\'>" % self.title

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AppPermission):
            return False

        return self.slug == other.slug

    def __hash__(self):
        return hash((self.slug,))

@dataclasses.dataclass(frozen=True)
class PermCategory:
    name: str
    identifier: str
    perms: list[AppPermission]


__categorized_permissions: list[PermCategory] = [
    PermCategory('Home', 'home', [
        AppPermission(slug='admin_tab', title="Admin Tab",
            desc="View the admin tab, including information on client referrals, contact growth, and workload.")
    ]),

    PermCategory('Contacts', 'contacts', [
        AppPermission(slug='contacts_access_all', title="Access To All Contacts",
            desc="Access to contacts the user is not assigned to, including their work, files, billing, and time."),

        AppPermission(slug='contacts_create_edit', title="Create and Edit Contacts",
            desc="Create new contacts in Canopy and edit existing contact information."),

        AppPermission(slug='manage_client_portals', title="Access \"Manage Client Portals\"",
            desc="Access to the \"manage client portals\" area of Canopy. See a holistic view of client portal users. "
                "Send and resend invitations in bulk. Remove access to the client portal."),

        AppPermission(slug='team_assign_contacts', title="Assign Contacts To Team Members",
            desc="Assign contacts to other team members."),

        AppPermission(slug='contacts_import', title="Import Contacts",
            desc="Import contacts from a CSV file."),

        AppPermission(slug='contacts_export', title="Export Contacts",
            desc="Export contacts to as CSV file."),

        AppPermission(slug='manage_contacts_status', title="Manage Active/Inactive Contacts",
            desc="Manage active/inactive status of contacts."),

        AppPermission(slug='contacts_email', title="Contact E-mail",
            desc="View and send e-mail correspondence to contacts the user has access to."),

        AppPermission(slug='contacts_bulk_email', title="Bulk E-mail",
            desc="Send bulk e-mails to contacts the user has access to."),

        AppPermission(slug='contacts_archive', title="Archive Contacts",
            desc="Archive contacts, removing them from the contact list."),

        AppPermission(slug='contacts_delete', title="Delete Contacts",
            desc="Permanently delete contacts from the archive."),
    ]),

    PermCategory('Work', 'work', [
        AppPermission(slug='work_crud', title="Create, Edit, and Assign Work",
            desc="Create new generic tasks, client requests, organizers, notices, eSignature requests, and subtasks in Canopy. "
            "Edit work details and assign work to other team members."),

        AppPermission(slug='generic_tasks', title="Generic Tasks",
            desc="View generic tasks the user has access to."),

        AppPermission(slug='client_requests_tasks', title="Send Client Request Tasks",
            desc="Send client request tasks directly to contacts the user has access to. "
            "Comment on client request tasks and send replies directly to contacts."),

        AppPermission(slug='tax_org', title="Tax Organizers",
            desc="View and manage tax organizers for contacts the user has access to."),

        AppPermission(slug='work_change_status', title="Change Work Status",
            desc="Change the status of generic tasks, client requests, organizers, notices, eSignature requests, and subtasks."),

        AppPermission(slug='work_export', title="Export Work",
            desc="Export all work on the tasks list to a CSV, including generic tasks, client requests, eSignature requests, and notices. "
            "Export tax organizers."),

        AppPermission(slug='work_archive', title="Archive Work",
            desc="Archive work, removing work from the tasks list and contact record."),

        AppPermission(slug='work_delete', title="Delete Work",
            desc="Permanently delete work from the archive."),
    ]),

    PermCategory('Engagements', 'engagements', [
        AppPermission(slug='engagements', title="Engagements",
            desc="View and manage tax resolution engagements. Create and send letters and engagement client requests directly to contacts."),
    ]),

    PermCategory('Files', 'files', [
        AppPermission(slug='contacts_files', title="Contact Files",
            desc="View and download files for contacts the user has access to."),

        AppPermission(slug='client_portal_visibility', title="Change Client Portal Visibility",
            desc="Make files visible in the client portal for contacts the user has access to."),

        AppPermission(slug='internal_files', title="Internal Files",
            desc="View and manage internal company files."),

        AppPermission(slug='files_upload', title="Upload, Move, & Organize Files",
            desc="Upload files to contacts, internal, and task workspaces.folders and rename folders."),

        AppPermission(slug='files_edit', title="Edit Files",
            desc="Edit files in Canopy with the Canopy Desktop Assistant."),

        AppPermission(slug='files_unlock', title="Unlock Files",
            desc="Unlock files locked by other users for editing."),

        AppPermission(slug='files_archive', title="Archive Files",
            desc="Archive files in contact and internal files, removing them from the files area."),

        AppPermission(slug='files_delete', title="Delete Files",
            desc="Permanently delete files from the archive."),
    ]),

    PermCategory('Transcripts', 'transcripts', [
        AppPermission(slug='transcripts', title="Transcripts",
            desc="View and manage transcripts for contacts the user has access to."),

        AppPermission(slug='transcripts_pull', title="Pull Transcripts",
            desc="Pull transcripts for contacts the user has access to."),
    ]),

    PermCategory('Billing', 'billing', [
        AppPermission(slug='invoices', title="Invoices",
            desc="View invoices for contacts the user has access to."),

        AppPermission(slug='invoices_ced', title="Create, Edit, & Send Invoices",
            desc="Create new and edit existing invoices for contacts the user has access to."),

        AppPermission(slug='payments', title="Payments",
            desc="View payments for contacts the user has access to."),

        AppPermission(slug='payments_edit', title="Create, Edit, & Refund Payments",
            desc="Create and edit payments for contacts the user has access to."),

        AppPermission(slug='credits', title="Credits",
            desc="View and manage credits for contacts the user has access to."),

        AppPermission(slug='statements', title="Statements",
            desc="Manage and generate statements for contacts the user has access to."),

        AppPermission(slug='reports', title="Reports",
            desc="View billing and time reports, such as revenue by team member and hours tracked by service item."),

        AppPermission(slug='billing_dashboard', title="Billing Dashboard/Revenue Reports",
            desc="View the billing dashboard, which includes outstanding invoices, year to date revenue reports, and recurring invoices."),

        AppPermission(slug='invoices_export', title="Export Invoices and Payments",
            desc="Export invoices and payments to CSV."),

        AppPermission(slug='invoices_archive_del', title="Archive & Delete Billing Items",
            desc="Archive and permanently delete billing items."),

        AppPermission(slug='wip_report', title="WIP Report",
            desc="View the Work-In-Progress report for billing"),
    ]),

    PermCategory('Time', 'time', [
        AppPermission(slug='time_team_saved', title="Team Member Saved Time",
            desc="View team members' time entries."),

        AppPermission(slug='time_user_edit', title="Edit Personal Time Entries",
            desc="Edit the user’s personal time entries."),

        AppPermission(slug='time_team_edit', title="Edit Team Member Time Entries",
            desc="Edit team members' time entries."),

        AppPermission(slug='productivity_dashboard', title="Productivity Dashboard",
            desc="View the productivity dashboard, which includes reports on hours logged on tasks, "
            "billed hours, and unbilled hours."),

        AppPermission(slug='time_export', title="Export Time Entries",
            desc="Export time entries to a CSV."),

        AppPermission(slug='time_archive', title="Archive Time Entries",
            desc="Archive time entries, removing them from the time entries card."),

        AppPermission(slug='time_delete', title="Delete Time Entries",
            desc="Permanently delete time entries from the archive."),
    ]),

    PermCategory('Templates', 'templates', [
        AppPermission(slug='tmpls_task', title="Task Templates",
            desc="View, manage, and create team templates for task workflows. Excludes private task templates."),

        AppPermission(slug='tmpls_folder', title="Folder Templates",
            desc="View, manage, and create custom folder structure templates."),

        AppPermission(slug='tmpls_email', title="E-mail Templates",
            desc="View, manage, and create team templates for e-mail. Excludes private e-mail templates."),

        AppPermission(slug='tmpls_letter', title="Letter Templates",
            desc="View, manage, and create templates for letters."),

        AppPermission(slug='tmpls_client', title="Client Request Templates",
            desc="View, manage, and create templates for client requests."),

        AppPermission(slug='tmpls_boilerplate', title="Boilerplate Text Templates",
            desc="View, manage, and create templates for boilerplate text."),

        AppPermission(slug='tmpls_portal_inv', title="Client Portal Invitation Templates",
            desc="View, manage, and create team templates for client portal invitations. "
            "Excludes private client portal invitation templates."),

        AppPermission(slug='tmpls_engagement', title="Engagement Templates",
            desc="View, manage, and create templates for tax resolution engagements."),

        AppPermission(slug='tmpls_notice', title="Notice Templates",
            desc="View, manage, and create templates for notices."),
    ]),

    PermCategory('Settings', 'settings', [
        AppPermission(slug='sett_comp_info', title="Company Information",
            desc="Access and edit company information, such as firm name, EIN, firm size, address, and phone number."),

        AppPermission(slug='sett_acc_mgmt', title="Account Management",
            desc="Assign licenses to team members, purchase credits, and edit company payment methods."),

        AppPermission(slug='sett_custom_brand', title="Custom Branding",
            desc="Edit custom branding, logo image, and client portal domain name."),

        AppPermission(slug='sett_custom_field', title="Custom Fields",
            desc="Manage and create custom fields for individuals and businesses."),

        AppPermission(slug='sett_tags', title="Tags",
            desc="View, create, and manage custom tags for tagging contacts."),

        AppPermission(slug='sett_team_member', title="Team Members",
            desc="View and edit team member information, add/delete team members, and assign team members to roles. "
            "View-only access to the roles and permissions area."),

        AppPermission(slug='sett_team_mem_salary', title="Team Member Salary",
            desc="View and edit team member salary and hourly rate."),

        AppPermission(slug='sett_roles', title="Roles and Permissions",
            desc="Edit roles and permissions."),

        AppPermission(slug='sett_integrations', title="Manage Integrations",
            desc="Manage and configure integrations."),

        AppPermission(slug='sett_billing', title="Billing and Payments",
            desc="Manage billing rates, service items, and your Canopy Payments merchant account."),

        AppPermission(slug='sett_log', title="Activity Log",
            desc="View events in the Activity Log"),
    ]),
]
# __categorized_permissions = []

__all_permissions: AppPermission = list(reduce(
    lambda a, b: a + b,
    map(lambda catd_perm: catd_perm.perms, __categorized_permissions),
    []
))

def categorized_permissions():
    return __categorized_permissions

def all_permissions(category=None):
    if category:
        return next((item.perms for item in __categorized_permissions if item.identifier == category), [])
    return __all_permissions

def find_permission_obj(slug: str) -> Optional[AppPermission]:
    return next((item for item in __all_permissions if item.slug == slug), None)

def find_permission_objs_many(*slugs: str) -> set[AppPermission]:
    return set(filter(lambda perm: perm.slug in slugs, __all_permissions))
