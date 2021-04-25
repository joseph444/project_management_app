from django.contrib import admin
from .models import Project,Subscriber


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


class SubscriberAdmin(admin.ModelAdmin):
    ordering = ('id',)
    search_fields = ['subscriber','project']
    list_display = ['subscriber','project']
    readonly_fields = ('created_at',)

    list_filter=()
    filter_horizontal=()
    fieldsets =()

    add_fieldsets =(
        (
            None,{
                'classes':('wide',),
                'fields':('subscriber','project')
            }
        )
    )

admin.site.register(Project,ProjectAdmin)
admin.site.register(Subscriber,SubscriberAdmin)