from django.contrib import admin
from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    ordering = ('id',)
    search_fields = ['project','name']
    list_display = ['name','project','registered_by','expense','created_at']
    readonly_fields = ('created_at',)

    list_filter=()
    filter_horizontal=()
    fieldsets=()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('project','registered_by','name' , 'description','expense'),
        }),
    )


admin.site.register(Expense,ExpenseAdmin)
# Register your models here.
