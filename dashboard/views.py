from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import UserProfile

from .decorators import profile_complete_required

from transaction.forms import LoanOrderForm
from transaction.models import LoanOrder, LoanOrderItem

import logging

logger = logging.getLogger('loanLogger')


@login_required
@profile_complete_required
def dashboard(request):
    if request.method == "POST":
        form = LoanOrderForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            loan_type = form.cleaned_data['loan_type']
            loan_amount = form.cleaned_data['loan_amount']
            loan_term = form.cleaned_data['loan_term']
            LoanOrder.create_loan_order(user_id, loan_type, loan_amount, loan_term)
            logger.info(
                f"User Id {user_id} took loan of type {loan_type} with loan amount {loan_amount} of term {loan_term}"
            )
    else:
        form = LoanOrderForm(initial={'loan_type': 'EL'})
    loan_order = []
    loan_order_items = []
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    try:
        loan_order = LoanOrder.objects.filter(user=user_profile, loan_status='processing', is_complete=False)[0]
        loan_order_items = LoanOrderItem.objects.filter(user=user_profile)
    except:
        pass
    context = {
        'user_profile': user_profile,
        'form': form,
        'loan_order': loan_order,
        'loan_order_items': loan_order_items,
    }

    return render(request, 'dashboard/dashboard.html', context)
