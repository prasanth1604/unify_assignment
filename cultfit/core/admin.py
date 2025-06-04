from django.contrib import admin
from .models import FitnessClass

class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'time', 'Instructor', 'total_slots')
    search_fields = ('name', 'Instructor')
    list_filter = ('time',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Exclude classes with no available slots
        return queryset

admin.site.register(FitnessClass, FitnessClassAdmin)