from django.contrib import admin

from .models import *


class LoanOrderAdmin(admin.ModelAdmin):
    list_display = ['loan_id', 'user', 'loan_status', 'loan_type', 'is_approved']
    list_filter = ['loan_status', 'is_approved', 'loan_type']
    search_fields = ['user__first_name', 'user__last_name', 'loan_id']


class LoanOrderItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(LoanOrder, LoanOrderAdmin)
admin.site.register(LoanOrderItem, LoanOrderItemAdmin)
