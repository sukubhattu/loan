from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class UserAdmin(UserAdmin):
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2', 'email')}),)
    form = UserChangeForm
    add_form = UserCreationForm


try:
    admin.site.unregister(User)
except:
    pass

admin.site.register(User, UserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
