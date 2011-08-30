from frontend.events.models import Event, Checkin, Message
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Event, EventAdmin)
admin.site.register(Checkin)
admin.site.register(Message)
