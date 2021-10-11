from functools import wraps

from django.contrib.auth.models import User
from users.models import UserProfile


def profile_complete_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user_id=request.user.id)
        if not user_profile.is_complete:

            print("Profile is not complete")
        else:
            print("Profile is  complete")
            return view_func(request, *args, **kwargs)

    return wrapper_func
