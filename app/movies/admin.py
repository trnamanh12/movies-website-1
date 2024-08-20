from django.contrib import admin
from .models import Movie, Review, Cinema, Screening, TicketType, Ticket, UserHistory
# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Cinema)
admin.site.register(Screening)
admin.site.register(TicketType)
admin.site.register(Ticket)
admin.site.register(UserHistory)