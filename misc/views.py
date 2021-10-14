from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse

import math
import stripe
import uuid

from .models import UserLoanInstallmentPaymentSession
from users.models import UserProfile
from transaction.models import LoanOrder, LoanOrderItem


def index(request):
    return render(request, 'misc/index.html')


def about(request):
    return render(request, 'misc/about.html')


@csrf_exempt
@login_required
def checkout_stripe(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
@login_required
def stripe_checkout_session(request):
    loan_order = []
    total = 0
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    try:
        loan_order = LoanOrder.objects.filter(user=user_profile, loan_status='processing', is_complete=False)[0]
        total = (loan_order.loan_amount / loan_order.loan_term) * 100
        total = math.trunc(total)
        total = str(total)
    except:
        pass
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:

            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                client_reference_id=loan_order.loan_id,
                line_items=[
                    {
                        'name': loan_order.loan_id,
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': total,
                    }
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required
def success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_loan_installment_payment_session_ids = list(
        UserLoanInstallmentPaymentSession.objects.values_list('session_id', flat=True)
    )
    try:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'])
        uuid_ = uuid.UUID(session['client_reference_id'])
        session_id = request.GET['session_id']
        paid_amount = session['amount_total'] / 100

        if session_id not in user_loan_installment_payment_session_ids and session['payment_status'] == 'paid':
            loan_order = LoanOrder.objects.get(loan_id=uuid_, is_complete=False)
            loan_order.loan_remaining_amount -= paid_amount
            loan_order.save()
            user_profile = UserProfile.objects.get(user_id=request.user.id)
            LoanOrderItem.objects.create(loan=loan_order, user=user_profile, installment_amount=paid_amount)

            if loan_order.loan_remaining_amount <= 0:
                loan_order.is_complete = True
                loan_order.save()
            UserLoanInstallmentPaymentSession.objects.create(session_id=session_id)

    except Exception as e:
        return redirect('misc:index')
    context = {'message': 'Thank you for paying your installment'}
    return render(request, 'misc/success.html', context)


@login_required
def cancelled(request):
    context = {'message': 'You cancelled your payment.'}
    return render(request, 'misc/cancel.html', context)
