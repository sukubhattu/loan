from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('profile-details', profile_details, name='details'),
    path('update_profile_details', update_profile_details, name='update_profile_details'),
]
