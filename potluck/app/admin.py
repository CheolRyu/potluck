from django.contrib import admin
from .models import Event, Guest, Friend, Item

# Register your models here.
admin.site.register(Event)
admin.site.register(Guest)
admin.site.register(Friend)
admin.site.register(Item)
