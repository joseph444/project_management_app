from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('name','project','assigned_to','deadline','created_at')
    search_fields = ('name','description','deadline')
    readonly_fields = ('created_at',)

    list_filter=()
    filter_horizontal=()
    fieldsets=()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('project','assigned_to','name','description','deadline','resources'),
        }),
    )

admin.site.register(Task,TaskAdmin)
