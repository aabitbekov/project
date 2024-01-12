from django.contrib import admin
from django.core.exceptions import ValidationError
from rangefilter.filters import DateRangeFilter
from django.utils.safestring import mark_safe
from .models import Signal, Incident
from .elastic_client_dev import getLast30Coincidence, getSignalsFromCoincidenceHits
from .readHits import readSignalsHits, readIncidentHits

# class HasIpSrcOrDstFilter(admin.SimpleListFilter):
#     title = 'ip-адрес'
#     parameter_name = 'dst или src'

#     def lookups(self, request, model_admin):
#         return (
#             ('dst', 'DST'),
#             ('src', 'SRC'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == 'dst':
#             return Incident.objects.filter(signals__ip_dst__isnull=True)    
#         elif self.value() == 'src':
#             return Incident.objects.exclude(signals__ip_dst__isnull=False)

class SignalAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'id', 'ip_src', 'ip_dst', 'user', 'uid')
    list_filter = ('ip_src', 'ip_dst')

class SignalInline(admin.TabularInline):  # или StackedInline
    model = Incident.signals.through
    extra = 1

class IncidentAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ip', 'matching_count'
                    , 'display_signals')
    search_fields = ['id', 'ip', 'signals__ip_src', 'signals__ip_dst']
    list_filter = ('timestamp', 'matching_count',
                    # HasIpSrcOrDstFilter, 
                #    ('timestamp', DateRangeFilter)
                   )
    inlines = [SignalInline]

    def get_queryset(self, request):
        hits, err = getLast30Coincidence()
        if err == None:
            signalHits, err = getSignalsFromCoincidenceHits(hits=hits)
            if err == None:
                signal_objects = readSignalsHits(signalHits)
                Signal.objects.all().delete()
                Signal.objects.bulk_create(signal_objects)
            else:
                raise ValidationError(f"Ошибка подключение к elastic/qainar-signals/: {err}")
        else:
            raise ValidationError(f"Ошибка подключение к elastic/qainar-coincidence/: {err}")    

        incident_objects = readIncidentHits(hits)
        return Incident.objects.all()

    def display_signals(self, obj):
        return mark_safe("<br>".join([str(related) for related in obj.signals.all()]))
    
    display_signals.short_description = 'Сигналы'






admin.site.register(Incident, IncidentAdmin)
admin.site.register(Signal, SignalAdmin)
