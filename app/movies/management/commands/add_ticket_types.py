from django.core.management.base import BaseCommand
from app.movies.models import TicketType

class Command(BaseCommand):
    help = 'Add ticket types to the database'

    def handle(self, *args, **kwargs):
        ticket_types = [
            {"name": "Standard", "price": 10.00},
            {"name": "VIP", "price": 20.00},
            {"name": "Student", "price": 8.00},
        ]

        for ticket_type in ticket_types:
            self.add_ticket_type(ticket_type["name"], ticket_type["price"])

    def add_ticket_type(self, name, price):
        ticket_type, created = TicketType.objects.get_or_create(name=name, defaults={'price': price})
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new TicketType: {ticket_type}"))
        else:
            self.stdout.write(self.style.WARNING(f"TicketType already exists: {ticket_type}"))