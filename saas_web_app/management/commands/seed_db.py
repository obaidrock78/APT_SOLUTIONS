from django.core.management.base import BaseCommand, CommandError

from auth_email_verify.actions import create_user
from auth_email_verify.models import AuthRole
from auth_email_verify.app_permissions import all_permissions, find_permission_obj, find_permission_objs_many

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):

        AuthRole.objects.all().delete()

        role_admin_regular = AuthRole.objects.create(name='Admin', label='admin_regular', rltype=AuthRole.RlType.BASIC)
        role_admin_no_bill = AuthRole.objects.create(name='Admin (No Billing)', label='admin_no_bill', rltype=AuthRole.RlType.BASIC)
        role_staff_all = AuthRole.objects.create(name='Staff (All Contacts)', label='staff_all', rltype=AuthRole.RlType.BASIC)
        role_staff_all_no_bill = AuthRole.objects.create(name='Staff (All Contacts, No Billing)', label='staff_all_no_bill', rltype=AuthRole.RlType.BASIC)
        role_staff_assigned = AuthRole.objects.create(name='Staff (Assigned Contacts)', label='staff_assigned', rltype=AuthRole.RlType.BASIC)
        role_staff_assigned_no_bill = AuthRole.objects.create(name='Staff (Assigned Contacts, No Billing)', 
            label='staff_assigned_no_bill', rltype=AuthRole.RlType.BASIC)

        all_perms_set = set(all_permissions())

        role_admin_regular.give_permissions_bulk(all_perms_set)
        role_admin_no_bill.give_permissions_bulk(
            all_perms_set 
            - set(all_permissions('billing'))
            - find_permission_objs_many('sett_team_mem_salary', 'sett_billing')
        )

        all_contacts = (
            set(all_permissions('contacts'))
            - find_permission_objs_many('manage_client_portals', 'contacts_import', 'contacts_bulk_email', 'contacts_delete')
        )
        assigned_contacts = all_contacts - find_permission_objs_many('contacts_access_all')

        no_billing = (
            set(all_permissions('work')) - find_permission_objs_many('work_delete')
            | set(all_permissions('engagements'))
            | set(all_permissions('files'))
            - find_permission_objs_many('files_unlock', 'files_delete')
            | set(all_permissions('transcripts'))
            | find_permission_objs_many('time_team_saved', 'time_user_edit', 'time_export', 'sett_tags')
        )

        with_billing = ( 
            no_billing
            | set(all_permissions('billing'))
            - find_permission_objs_many('reports', 'billing_dashboard', 'invoices_archive_del', 'wip_report')
        )

        role_staff_all.give_permissions_bulk(with_billing | all_contacts)
        role_staff_all_no_bill.give_permissions_bulk(no_billing | all_contacts)

        role_staff_assigned.give_permissions_bulk(with_billing | assigned_contacts)
        role_staff_assigned_no_bill.give_permissions_bulk(no_billing | assigned_contacts)

        admin = create_user('Admin', 'admin', 'pass', True, True)
        user1 = create_user('User 1', 'user1', 'pass', True, False)
        user2 = create_user('User 2', 'user2', 'pass', True, False)
        user3 = create_user('User 3', 'user3', 'pass', True, False)

        admin.role = role_admin_regular
        admin.save()

        user1.role = role_staff_all
        user2.role = role_staff_all
        user3.role = role_staff_all

        user1.save()
        user2.save()
        user3.save()