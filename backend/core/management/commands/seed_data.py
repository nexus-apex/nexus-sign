from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Document, SignRequest, Template
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusSign with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexussign.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Document.objects.count() == 0:
            for i in range(10):
                Document.objects.create(
                    title=f"Sample Document {i+1}",
                    sender=f"Sample {i+1}",
                    status=random.choice(["draft", "sent", "viewed", "signed", "declined", "expired"]),
                    signers=random.randint(1, 100),
                    sent_date=date.today() - timedelta(days=random.randint(0, 90)),
                    completed_date=date.today() - timedelta(days=random.randint(0, 90)),
                    file_url=f"https://example.com/{i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Document records created'))

        if SignRequest.objects.count() == 0:
            for i in range(10):
                SignRequest.objects.create(
                    document_title=f"Sample SignRequest {i+1}",
                    signer_name=f"Sample SignRequest {i+1}",
                    signer_email=f"demo{i+1}@example.com",
                    status=random.choice(["pending", "signed", "declined"]),
                    sent_date=date.today() - timedelta(days=random.randint(0, 90)),
                    signed_date=date.today() - timedelta(days=random.randint(0, 90)),
                    ip_address=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 SignRequest records created'))

        if Template.objects.count() == 0:
            for i in range(10):
                Template.objects.create(
                    name=f"Sample Template {i+1}",
                    category=f"Sample {i+1}",
                    pages=random.randint(1, 100),
                    fields_count=random.randint(1, 100),
                    usage_count=random.randint(1, 100),
                    active=random.choice([True, False]),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Template records created'))
