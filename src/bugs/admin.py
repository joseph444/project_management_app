from django.contrib import admin
from .models import Bug

class BugAdmin(admin.ModelAdmin):
    ordering = ('id',)
    search_fields = ['project','name']
    list_display = ['name','project','task','registered_by','created_at']
    readonly_fields = ('created_at',)

    list_filter=()
    filter_horizontal=()
    fieldsets=()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','project','task','registered_by','description','reproduce','is_close'),
        })
    )
    

admin.site.register(Bug,BugAdmin)


