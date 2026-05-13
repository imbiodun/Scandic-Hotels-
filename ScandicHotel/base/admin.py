from django.contrib import admin
from .models import Amenity, Room, DiscountCode, Reservation

# Register your models here.
admin.site.register(Amenity)
admin.site.register(Room)
admin.site.register(DiscountCode)
admin.site.register(Reservation)
