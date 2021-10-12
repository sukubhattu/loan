from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import UserProfile

from .decorators import profile_complete_required

from transaction.forms import LoanOrderForm
from transaction.models import LoanOrder


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
    else:
        form = LoanOrderForm(initial={'loan_type': 'EL'})
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    context = {'user_profile': user_profile, 'form': form}
    return render(request, 'dashboard/dashboard.html', context)
