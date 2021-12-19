from django.core.management.base import BaseCommand, CommandError

from auth_email_verify.actions import create_user

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