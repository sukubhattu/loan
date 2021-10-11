from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse

from datetime import datetime
from django.utils import dateparse
from django.utils.dateparse import parse_date
from .models import UserProfile


@login_required
def profile_details(request):
    return render(request, 'users/profile_details.html')


@login_required
def update_profile_details(request):
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user_id=request.user.id)
        request_data = request.POST
        try:
            dob = request_data['dob']
            dob = datetime.strptime(dob, "%Y-%m-%d").date()
            print(dob)
            user_profile.first_name = request_data['firstname']
            user_profile.last_name = request_data['lastname']
            user_profile.address = request_data['address']
            user_profile.gender = request_data['gender']
            user_profile.dob = dob
            user_profile.contact_number = int(request_data['contactNumber'])
            user_profile.loan_amount = float(request_data['loanAmount'])
            user_profile.loan_term = int(request_data['loanTerm'])
            user_profile.installment_amount = float(request_data['installmentAmount'])

            user_profile.is_complete = True
            user_profile.save()
            response = {'message': 'Post received'}
        except:
            data = {'result': 'error', 'message': 'Form invalid', 'form': 'oops.'}
            return JsonResponse(data, status_code=400)
    else:
        response = {'message': 'Thank you for visiting this URL'}
    return JsonResponse(response)
