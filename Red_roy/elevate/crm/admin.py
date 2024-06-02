# crm/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, BlogPost,Reservation,BlogImage,ReservationClient

# Register the CustomUser model using the built-in UserAdmin
class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event)
admin.site.register(BlogPost)
admin.site.register(Reservation)
admin.site.register(BlogImage)
admin.site.register(ReservationClient)
