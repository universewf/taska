from django.contrib import admin


from application.models import Reservation, Table
# Register your models here.

admin.site.register(Table)
admin.site.register(Reservation)