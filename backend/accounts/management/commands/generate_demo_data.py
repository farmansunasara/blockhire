"""
Management command to generate demo data for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from documents.models import DocumentRecord
from verification.models import VerificationRequest
from issuer.models import Issuer, IssuerAuthorization
import random
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate demo data for testing'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--issuers', type=int, default=3, help='Number of issuers to create')

    def handle(self, *args, **options):
        num_users = options['users']
        num_issuers = options['issuers']

        # Create demo users
        self.stdout.write('Creating demo users...')
        users = []
        for i in range(num_users):
            user = User.objects.create_user(
                email=f'demo{i+1}@example.com',
                username=f'demo{i+1}@example.com',
                password='demo123',
                first_name=f'Demo{i+1}',
                last_name='User'
            )
            
            # Create profile
            profile = UserProfile.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                date_of_birth='1990-01-01',
                mobile=f'+123456789{i}',
                address=f'{100+i} Demo Street, Demo City',
                job_designation=f'Software Engineer {i+1}',
                department='Engineering',
                is_profile_complete=True
            )
            
            users.append(user)
            self.stdout.write(f'Created user: {user.email}')

        # Create demo issuers
        self.stdout.write('Creating demo issuers...')
        issuers = []
        for i in range(num_issuers):
            issuer = Issuer.objects.create(
                issuer_id=f'ISSUER_{i+1}',
                name=f'Demo Issuer {i+1}',
                email=f'issuer{i+1}@demo.com',
                company=f'Demo Company {i+1}'
            )
            issuers.append(issuer)
            self.stdout.write(f'Created issuer: {issuer.name}')

        # Create some authorizations
        self.stdout.write('Creating authorizations...')
        for issuer in issuers:
            for user in users[:3]:  # Authorize first 3 users
                IssuerAuthorization.objects.create(
                    issuer=issuer,
                    emp_id=user.emp_id,
                    user_hash=user.user_hash,
                    employee=user,
                    status='approved',
                    permission_granted=True,
                    granted_at=datetime.now(),
                    created_by=user
                )

        # Create some verification requests
        self.stdout.write('Creating verification requests...')
        for user in users[:5]:  # First 5 users
            VerificationRequest.objects.create(
                emp_id=user.emp_id,
                doc_hash='demo_hash_' + str(random.randint(1000, 9999)),
                requested_by=user,
                status='verified',
                is_valid=True,
                verification_date=datetime.now(),
                result_message='Demo verification successful',
                request_ip='127.0.0.1'
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Demo data created successfully: {num_users} users, {num_issuers} issuers'
            )
        )
