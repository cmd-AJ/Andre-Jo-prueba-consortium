import json
from django.core.management.base import BaseCommand
from liquidations.models import Liquidation
from django.contrib.auth import get_user_model
from datetime import datetime

class Command(BaseCommand):
    help = 'Load data from JSON file into the Liquidation model'

    def handle(self, *args, **kwargs):
        with open('fixtures/db/liquidations.json', 'r') as f:
            data = json.load(f)

        for item in data:
            fields = item.get('fields')
            creator = get_user_model().objects.get(id=fields['creator'])  # Adjust if needed
            
            liquidation = Liquidation.objects.create(
                created=datetime.strptime(fields['created'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                creator=creator,
                document_type_code=fields['document_type_code'],
                invoice_nit=fields['invoice_nit'],
                invoice_serie=fields['invoice_serie'],
                invoice_number=fields['invoice_number'],
                invoice_name=fields['invoice_name'],
                invoice_adress=fields['invoice_adress'],
                total_value=fields['total_value'],
                description=fields['description'],
                document_link=fields['document_link'],
                state=fields['state'],
                is_devolution=fields['is_devolution'],
                elimination_reason=fields['elimination_reason'],
                document=fields['document'] if fields['document'] else None
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully added liquidation {liquidation.pk}"))
