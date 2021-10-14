from django.contrib import admin

from .models import *


class LoanOrderAdmin(admin.ModelAdmin):
    model = LoanOrder
    list_display = ['loan_id', 'user', 'loan_status', 'loan_type', 'is_approved', 'is_complete']
    list_filter = ['loan_status', 'is_approved', 'is_complete', 'loan_type']
    search_fields = ['user__first_name', 'user__last_name', 'loan_id']


class LoanOrderItemAdmin(admin.ModelAdmin):
    model = LoanOrderItem
    list_display = ['loan']


admin.site.register(LoanOrder, LoanOrderAdmin)
admin.site.register(LoanOrderItem, LoanOrderItemAdmin)
