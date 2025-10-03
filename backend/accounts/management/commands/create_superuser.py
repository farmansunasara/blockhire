"""
Management command to create a superuser with custom fields.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with custom fields'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email address')
        parser.add_argument('--password', type=str, help='Password')
        parser.add_argument('--first-name', type=str, help='First name')
        parser.add_argument('--last-name', type=str, help='Last name')

    def handle(self, *args, **options):
        email = options.get('email') or input('Email: ')
        password = options.get('password') or input('Password: ')
        first_name = options.get('first_name') or input('First name: ')
        last_name = options.get('last_name') or input('Last name: ')

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f'User with email {email} already exists')
            )
            return

        user = User.objects.create_superuser(
            email=email,
            username=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create profile
        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            date_of_birth='1990-01-01',
            mobile='+1234567890',
            address='Admin Address',
            job_designation='Administrator',
            department='IT',
            is_profile_complete=True
        )

        self.stdout.write(
            self.style.SUCCESS(f'Superuser {email} created successfully')
        )
