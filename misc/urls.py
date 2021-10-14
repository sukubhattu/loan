from django.urls import path
from .views import *

app_name = 'misc'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('checkout_stripe', checkout_stripe, name='checkout_stripe'),
    path('stripe_checkout_session', stripe_checkout_session, name='stripe_checkout_session'),
    path('success/', success),
    path('cancelled/', cancelled),
]
