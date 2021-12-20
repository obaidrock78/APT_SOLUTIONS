from django.core.management.base import BaseCommand, CommandError

from auth_email_verify.actions import create_user
from auth_email_verify.models import AuthRole

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        create_user('Admin', 'admin', 'pass', True, True)
        create_user('User 1', 'user1', 'pass', True, False)
        create_user('User 2', 'user2', 'pass', True, False)
        create_user('User 3', 'user3', 'pass', True, False)


        self.create_basic_roles()


    def create_basic_roles(self):
        AuthRole.objects.all().delete()

        """
            Admin
            Admin (No Billing)
            Staff (All Contacts)
            Staff (All Contacts, No Billing)
            Staff (Assigned Contacts)
            Staff (Assigned Contacts, No Billing)
        """

        AuthRole.objects.create(name='Admin', label='admin_regular', rltype=AuthRole.RlType.BASIC)
        AuthRole.objects.create(name='Admin (No Billing)', label='admin_no_bill', rltype=AuthRole.RlType.BASIC)
        AuthRole.objects.create(name='Staff (All Contacts)', label='staff_all', rltype=AuthRole.RlType.BASIC)
        AuthRole.objects.create(name='Staff (All Contacts, No Billing)', label='staff_all_no_bill', rltype=AuthRole.RlType.BASIC)
        AuthRole.objects.create(name='Staff (Assigned Contacts)', label='staff_assigned', rltype=AuthRole.RlType.BASIC)
        AuthRole.objects.create(name='Staff (Assigned Contacts, No Billing)', label='staff_assigned_no_bill', rltype=AuthRole.RlType.BASIC)
