from django.core.management.base import BaseCommand
from orders.models import IngredientOrderItem

class Command(BaseCommand):
    help = 'Update existing order items to set added_by to orderer'

    def handle(self, *args, **options):
        # Get all order items with no added_by user set
        items = IngredientOrderItem.objects.filter(added_by__isnull=True)
        count = 0
        
        for item in items:
            # Set the added_by to the orderer of the order
            item.added_by = item.order.orderer
            item.save()
            count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} items')) 