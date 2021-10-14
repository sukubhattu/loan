from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import JsonResponse

from datetime import datetime
from django.utils import dateparse
from django.utils.dateparse import parse_date

from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile_details(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = UserProfile.objects.get(user_id=request.user.id)
            data_to_be_updated = {
                "first_name": form.cleaned_data['first_name'],
                "last_name": form.cleaned_data['last_name'],
                "address": form.cleaned_data['address'],
                "gender": form.cleaned_data['gender'],
                "date_of_birth": form.cleaned_data['date_of_birth'],
                "contact_number": form.cleaned_data['contact_number'],
                "loan_amount": form.cleaned_data['loan_amount'],
                "loan_term": form.cleaned_data['loan_term'],
                "installment_amount": form.cleaned_data['installment_amount'],
                "is_complete": True,
            }
            for key, value in data_to_be_updated.items():
                setattr(user_profile, key, value)
            user_profile.save()
            return redirect('dashboard:dashboard')
    else:
        form = UserProfileForm(initial={'gender': 'Male'})
    return render(request, 'users/profile_details.html', {'form': form})


# This API is depreciated for now.
# Currently this API does not support proper validation
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
