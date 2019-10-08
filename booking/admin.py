from django.contrib import admin
from .models import Ticket, Pricing


# Register your models here
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'name','phone_no','to','origin','date_of_departure','time_of_departure','seat_no','price']

admin.site.register(Ticket, TicketAdmin)

class PricingAdmin(admin.ModelAdmin):
    list_display = ['origin', 'to','price']

admin.site.register(Pricing, PricingAdmin)
