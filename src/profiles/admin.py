from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    ordering = ('id',)
    search_fields = ['username']
    list_display = ['username','role','user_id','created_at']
    readonly_fields = ('created_at',)

    list_filter=()
    filter_horizontal=()
    fieldsets=()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id','role','pro_picture' , 'username','bio'),
        }),
    )

admin.site.register(Profile,ProfileAdmin)