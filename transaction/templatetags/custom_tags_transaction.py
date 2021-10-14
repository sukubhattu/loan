from django import template

register = template.Library()

from users.models import UserProfile
from transaction.models import LoanOrder


@register.filter(name='get_loan_status')
def get_loan_status(user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    loan_orders = LoanOrder.objects.filter(user=user_profile, loan_status='processing', is_complete=False)
    return loan_orders
