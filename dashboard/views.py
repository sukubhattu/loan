from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .decorators import profile_complete_required


@login_required
@profile_complete_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
