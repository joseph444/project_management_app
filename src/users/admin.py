from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users


class AdminUser(UserAdmin):
    ordering = ('email',)
    list_display = ('email','first_name','last_name','date_joined','last_login','is_admin','is_staff')
    search_fields = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')

    list_filter=()
    filter_horizontal=()
    fieldsets=()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name' , 'password1', 'password2'),
        }),
    )



admin.site.register(Users,AdminUser)
    
# Register your models here.
