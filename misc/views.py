from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
import stripe

from .models import UserLoanInstallmentPaymentSession


def index(request):
    return render(request, 'misc/index.html')


@csrf_exempt
@login_required
def checkout_stripe(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
@login_required
def stripe_checkout_session(request):
    customer = request.user
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:

            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'mero bill amout',
                        'quantity': 1,
                        'currency': 'aud',
                        'amount': 2000,
                    }
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required
def success(request):
    # stripe.api_key = settings.STRIPE_SECRET_KEY
    # customer = request.user

    # user_loan_installment_payment_session_ids = list(
    #     UserLoanInstallmentPaymentSession.objects.values_list('session_id', flat=True)
    # )
    # try:
    #     session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    #     session_id = request.GET['session_id']
    #     if session_id not in user_loan_installment_payment_session_ids and session['payment_status'] == 'paid':
    #         # logic to decrease amount
    #         UserLoanInstallmentPaymentSession.objects.create(session_id=session_id)

    # except Exception as e:
    #     return redirect('misc:index')
    context = {'message': 'Thank you for paying your installment'}
    return render(request, 'misc/success.html', context)


@login_required
def cancelled(request):
    context = {'message': 'You cancelled your payment.'}
    return render(request, 'misc/cancel.html', context)
