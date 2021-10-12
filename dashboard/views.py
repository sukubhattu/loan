from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import UserProfile

from .decorators import profile_complete_required


@login_required
@profile_complete_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    context = {'user_profile': user_profile}
    return render(request, 'dashboard/dashboard.html', context)
