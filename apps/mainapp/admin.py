# Register your models here.
from django.contrib import admin
from .models import *

    

class SignalInline(admin.TabularInline):  # или StackedInline
    model = Incident.signals.through
    extra = 1

class IncidentAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ip', 'matching_count')
    search_fields = ['id', 'ip']
    list_filter = ('timestamp', 'matching_count')
    inlines = [SignalInline]

    


admin.site.register(Incident, IncidentAdmin)
admin.site.register(Signal)
