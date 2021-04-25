from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    ordering = ('id',)
    search_fields = ['project_name','slug']
    list_display = ['project_name','user_id','budget','created_at']
    readonly_fields = ('created_at','slug')

    list_filter=()
    filter_horizontal=()
    fieldsets=()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id','project_name','budget','description'),
        }),
    )


admin.site.register(Project,ProjectAdmin)